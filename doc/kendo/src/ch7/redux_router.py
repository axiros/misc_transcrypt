from tools import d, jd, dumps, log, die


__pragma__('alias', 'jq', '$') # only for ajax, replace maybe with sth lighter
__pragma__('alias', 'lodash', '_') # only for ajax, replace maybe with sth lighter

def build_store_id( prefix, target, sel):
     """
     comp = {comp: 'App', 'state': {...} -> build an id from
     comp. type and principal state """
     id = [prefix + sel + '.' + target.cls]
     s = target.state
     if not s:
         return id[0]
     for k, v in dict(s).items():
         if not k in ('_id_', 'data'):
             id.extend([k, v])
     id =  '.'.join(id)
     return id

class ReduxRouter:

    def find_class(self, container, cls):
        ''' find the class by string '''
        p = container
        while p:
            c = p[cls]
            if c:
                return c
            p = p._container
        die(cls, 'not found in', container)


    def flatten(self, route_upd_tree, g, prefix, container, ns, reg):
        """
        recursing into a route_upd_tree: hirarch. tree, i.e. a route upd.
        - rebuilding the (flat) current route dict `g` for all routes starting
            with `prefix`
        - deleting existing and creating new instances while we traverse

        """



        for sel, target in route_upd_tree.items():
            instance = container

            log(sel)

            ks = g.keys()
            if prefix != '':
                prefix += '.'

            keys =  [k for k in ks if k.startswith(prefix + sel)]

            if target == False or 'cls' in target:
                for k in keys:
                    del g[k]
                    if k in ns:
                        log('store delete', k)
                        del ns[k]
                if target == False:
                    continue
            else:
                # take old - its the shortest with that `prefix`:
                keys.sort()
                store_id = keys[0]

            if 'cls' in target:

                # target not just {'#sel1: {...}, '#sel2': {}, but also
                # parametrizing an instance at the cur. selector.

                store_id = build_store_id(prefix, target, sel)
                g[store_id] = lodash.merge({}, g[store_id])

                instance = reg[store_id]
                if instance:
                    log('instance', store_id, 'already in registry')
                else:
                    log('store add', store_id)
                    # clone
                    g[store_id]['_id_'] = 1

                    cls = self.find_class(container, target.cls)
                    instance = cls( id         = store_id,
                                    app        = self,
                                    select     = sel,
                                    init_state = g[store_id],
                                    container  = container)

                    reg[store_id] = instance

                ns[store_id] = g[store_id]

            for sub_sel in target.keys():
                if sub_sel in ('state', 'cls'):
                    continue
                self.flatten({sub_sel: target[sub_sel]}, g, store_id,
                                                         instance, ns, reg)

    def reduce_route_update(self, ns, action):
        """ reducer received route update """

        reg = self.components_by_id
        route_upd = dict(action.data.route)

        g = ns.route
        self.flatten(route_upd, g, '', self, ns, reg)
        log('flat route now:')
        dumps(g)
        ns.route = g
        return ns

