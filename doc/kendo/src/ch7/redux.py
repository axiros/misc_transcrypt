from tools import d, dj, dumps, log


__pragma__('alias', 'jq', '$') # only for ajax, replace maybe with sth lighter
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


# app = globally available:
#app = ReduxApp()
#app.store.dispatch(d(type='test', data=d(foo='bar')))

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
    __state_id__ = 0
    _app = _container = None
    lc_state = LC.new

    def __init__(self, kw):
        self.id         = kw.id
        self._app       = kw.app
        self._container = kw.container
        self.select     = kw.select
        self.state      = kw.init_state or {}
        self.register()

    def register(self):
        if not self.id: # set by the router normally
            self.id = self.__class__.__name__ + '_' + time.time()
        if not self.state:
            self.state = {}
        # state id, updated at each change. useful for quick diffs in the
        # update_all:
        self.state['_id_'] = self.__state_id__

        self._app.register_component(self)

    def __repr__(self):
        s = self.id
        if self.select:
            s += '@' + self.select
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
        self.set_state(LC.unmounted)

    def ajax(self, meth, send, url):
        self._app.ajax(self, meth, send, url)

    def get_data(self):
        self.ajax('get', {}, self.url)

    def got_data(self):
        self.requesting_data = False
        log(self, 'have new data')
        self.update()


class ReduxApp:
    id = 'app'
    store = s_store = None
    components_by_id = None

    def __init__(self, init_state):
        self.init_state = init_state or {}
        self.create_store_and_components_registry()
        if 'r_state' in self:
            self.start_router()

    def create_store_and_components_registry(self):
        self.components_by_id = {}
        self.store = create_redux(self.reducer, self.init_state)
        # s_ -> a stream
        self.s_store = ReduxKefir.createProjection(self.store)
        self.s_store.onValue(self.update_components)
        # we are also a component, our app = self:


    def dispatch(self, type, comp_id, kvs):
        ''' updating of a single components state '''
        # will trigger call of redux to reducer:
        self.store.dispatch({'type': type, 'data': {comp_id: kvs}})

    def reducer(self, state, action):
        ''' job of this one is to build a new state for the store, based on its
        current state and an action with type and state data '''
        console.log('reducer, type:', action.type, 'action.data:')
        dumps(action.data)

        ns = {}        # new state - from old state:
        ns.update(state)
        # and action data:
        d = action.data
        if not d:
            return ns

        ns['action'] = action.type
        for comp_id, kv in d.items():
            # deep copy for route updates
            if comp_id == 'route':
                m = {}
                have = ns.route
                if not have:
                    have = {}
                jq.extend(m, have, kv)
                ns.route = m
                continue

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
        """ called from store observer """
        s_log(x)
        s = self.store.getState()
        for id, comp in self.components_by_id.items():
            #if id == 'xApp.Comp1.id1.bar.Comp2.id2.foo':
            #    debugger
            store_cstate = s[id]
            if not store_cstate:
                # slider back in time:
                if not comp.__state_id__ == -1:
                    comp.unmount()
                comp.__state_id__ = -1
                continue
            if comp.__state_id__ != store_cstate._id_:
                data = store_cstate.data
                # convenience for the comps: provide a got_data hook ,saves
                # some ifs in the comps:
                if data and comp.state.data != data:
                    comp.state = store_cstate
                    comp.got_data()
                else:
                    comp.state = store_cstate
                    comp.update()
                comp.__state_id__ = store_cstate._id_

        rs = self.r_state
        if rs == self.r_active:
            return
        call = 0
        if s.action == 'server_data' and rs == self.r_waiting:
            call = 1
        if s.route != self.cur_route and rs == self.r_inactive:
            call = 1
        if call:
            console.log('calling router')
            self.set_router_state(self.r_active)
            self.realize_route(self, s.route)
            if self.r_state != self.r_waiting:
                self.cur_route = s.route
                self.set_router_state(self.r_inactive)


    def register_component(self, comp):
        self.components_by_id[comp.id] = comp
        # here, app may still freely mutate the state, e.g. pull from server:
        # via self.ajax, we have the comp object
        # for now we accept it as is, and this will trigger the comp.update:
        self.dispatch('comp.init', comp.id, comp.state)


    def ajax(self, comp, meth, send, url):
        def success(data, mode, props):
            id, app = this.comp.id, self
            app.dispatch('server_data', id, dj(data=data))

        opts = dj(type=meth, url=url,
                dataType='json', data=send,
                success=success, error=success,
                context=dj(comp=comp, app=self))
        jq.ajax(opts)

