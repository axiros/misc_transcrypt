from tools import d, jd, dumps, log, die
from redux_router import ReduxRouter


__pragma__('alias', 'jq', '$') # only for ajax, replace maybe with sth lighter
__pragma__('alias', 'lodash', '_') # only for ajax, replace maybe with sth lighter
def s_log(x):
    """stream log """
    console.log('store stream event. store current state:', x)

def create_redux(reducer, init_state):
    c, k = Redux.createStore, ReduxKefir.observableMiddleware
    c = Redux.applyMiddleware(k)(c)
    wd = window.devToolsExtension
    if wd:
        return c(reducer, init_state, wd())
    else:
        return c(reducer, init_state)

import time
class LC:
    new = 'new'
    updating     = 'updating'
    updated      = 'updated'
    getting_data = 'getting_data'
    unmounted    = 'unmounted'

class ReduxComponent:
    '''
    A ReduxApp Component with

    - an id
    - serializable primary state

    state can be set by the app, also async.
    '''
    id = state = select = None # mp mountpoint, selector is reserved by TS
    # state id, updated at each change. useful for quick diffs in the
    __state_id__ = 0
    _app = _container = None
    lc_state = LC.new

    def __init__(self, kw):
        self.id         = kw.id
        self._app       = kw.app
        self._container = kw.container
        self.select     = kw.select
        self.state      = kw.init_state or {}
        self.preregister()
        self.register()

    def preregister(self):
        ''' hook'''
        pass

    def register(self):
        if not self.id: # set by the router normally
            self.id = self.__class__.__name__ + '_' + time.time()
        if not self.state:
            self.state = {}

        self._app.register_component(self)

    def __repr__(self):
        s = self.id
        #if self.select:
        #    s += '@' + self.select
        s += '[' + self.lc_state + ']'
        return s

    def set_state(self, mode):
        log(self, 'setting state', mode)
        self.lc_state = mode

    def update(self):
        """ in zope this would be __set_state__ -
        we have our state and create the view """
        self.set_state(LC.updating)
        log(self, 'update, state:', self.state)
        self.dom_update()
        self.set_state(LC.updated)

    def unmount(self):
        self.dom_revert()
        self.__state_id__ = 0
        self.set_state(LC.unmounted)

    def ajax(self, meth, send, url):
        self._app.ajax(self, meth, send, url)

    def get_data(self):
        self.ajax('get', {}, self.url)

    def got_data(self):
        self.requesting_data = False
        log(self, 'have new data')
        self.update()


    def mount_sub(self, select, cls, state):
        '''dispatching a route action which leads to a mounted subcomponent '''
        # where are we in the current route?
        s = self._app.get_state().route
        parents = self._app.parents(self)
        route = full_route = {}
        for p in parents:
            m = {}
            route[p.select] = m
            route = m
        route[select] = {'cls': cls}
        if state:
            route[select]['state'] = state
        self._app.baz = 1
        self._app.dispatch('route_update', 'route', full_route)

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

class ReduxApp(ReduxRouter):
    id = 'app'
    store = s_store = None
    components_by_id = None

    def __init__(self, init_state):
        self.init_state = init_state or {}
        self.create_store_and_components_registry()

    def create_store_and_components_registry(self):
        self.components_by_id = {}
        self.store = create_redux(self.reducer, self.init_state)
        # s_ -> a stream
        self.s_store = ReduxKefir.createProjection(self.store)
        self.s_store.onValue(self.update_components)
        # we are also a component, our app = self:

    def get_state(self):
        return self.store.getState()

    def dispatch(self, type, comp_id, kvs):
        ''' updating of a single components state '''
        # will trigger call of redux to reducer:
        self.store.dispatch({'type': type, 'data': {comp_id: kvs}})


    def reducer(self, state, action):
        ''' job of this one is to build a new state for the store, based on its
        current state and an action with type and state data '''
        console.log('reducer, type:', action.type, 'action.data:')
        dumps(action.data)

        ns = {'route': {}}        # new state - from old state:
        ns.update(state)
        # and action data:
        if not action.data:
            # init:
            return ns

        ns['action'] = action.type
        if action.type == 'route_update':
            return self.reduce_route_update(ns, action)

        # normal state changes:
        for comp_id, kv in action.data.items():
            #if action.type == 'life_cycle':
            #    if len(d.unmount):
            #        # kick its id from the new state, so that by the observer
            #        # it will be unmounted:
            #        for id in d.unmount:
            #            if id in ns:
            #                del ns[id]
            #        continue

            comp = self.components_by_id[comp_id]
            # for comps we know copy level, theirs are flat:
            if comp:
                cstate = comp.state
                cns = {} # new component state
                cns.update(cstate)
                cns.update(kv)
                cns['_id_'] += 1
                ns[comp_id] = cns
        return ns

    def update_components(self, x):
        """
        Called from store observer

        The store should at this point just have instantiated comps
        which must be in the DOM.
        So do this now, update the DOM.

        We go through all in the reg.
        Check if in the store:
            if not: unmount if not already unmounted
            if in:  mount if not already mounted

        Complication: Comps which need data, but have subcomps
        (e.g. from a copied route with data present, in the new browser the data
        must be pulled first to mount the subcomp).
        Here we break the process for the sub comps and start the data fetch.
        """
        s_log(x)
        reg = self.components_by_id
        ids = reg.keys()
        s = self.get_state()
        __pragma__('js', '{}', 'var ids_rev = ids.reverse()')

        # unmount from longest to shortest:
        for id in ids_rev:
            if not id in s:
                comp = reg[id]
                if comp.lc_state != LC.unmounted:
                    if self.bar:
                        debugger
                    reg[id].unmount()

        # now top down instantiation:
        delayed = []
        __pragma__('js', '{}', 'var ids = ids_rev.sort()')
        for id in ids:
            state = s[id]
            if not state or id in delayed:
                # not in store
                continue
            comp = reg[id]
            if not comp:
                console.log('skipping - not in store', id)
                continue
            if comp.lc_state == LC.new:
                comp.update()
            elif comp.__state_id__ != state._id_:
                data = state.data
                # convenience for the comps: provide a got_data hook ,saves
                # some ifs in the comps:
                comp.state = state
                if data and s['action'] == 'server_data':
                    comp.got_data()
                else:
                    comp.update()
            comp.__state_id__ = state._id_

            if comp.url and not 'data' in state:
                if hasattr(comp, 'auto_data'):
                    if comp.requesting_data == True:
                        pass
                    else:
                        comp.get_data()
                comp.requesting_data = True
            if comp.requesting_data:
                delayed.extend([i for i in ids if i.startswith(comp.id)])


    def ajax(self, comp, meth, send, url):
        def success(data, mode, props):
            id, app = this.comp.id, self
            app.dispatch('server_data', id, jd(data=data))
        def error(data, mode, props):
            die("ServerComm", 'no data', comp.id, comp.url, props)

        opts = jd(type=meth, url=url,
                  dataType='json', data=send,
                  success=success, error=error,
                  context=jd(comp=comp, app=self))
        jq.ajax(opts)



    # ------------------------------------------------------ registry functions
    def register_component(self, comp):
        console.log('registering', comp.id)
        self.components_by_id[comp.id] = comp
        # here, app may still freely mutate the state, e.g. pull from server:
        # via self.ajax, we have the comp object
        # for now we accept it as is, and this will trigger the comp.update:
        #self.dispatch('comp.init', comp.id, comp.state)

    def get_subs(self, container, select, excl_id, deep):
        ''' get all sub components of a component '''
        if not excl_id:
            excl_id = 'xxx'
        cid = container.id
        subs = [ [id, c] for id, c in self.components_by_id.items() \
                 if id.startswith(cid) and not id in [excl_id, cid] ]
        if not select:
            return subs

        ssubs = [[id, c] for id, c in subs if c.select == select]
        if not deep:
            return ssubs
        ret = []

        for cid, ccomp in ssubs:
            ret.extend([[id, c] for id, c in subs if c.id.startswith(cid)])

        return ret


    def parents(self, comp):
        parents = []
        p = comp
        while p != comp._app:
            parents.insert(0, p)
            p = p._container
        return parents
