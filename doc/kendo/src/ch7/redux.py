from tools import d, dj

__pragma__('alias', 'jq', '$') # only for ajax, replace maybe with sth lighter
def s_log(x):
    """stream log """
    console.log('stream value', x)

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

    def __init__(self, kw):
        self.id         = kw.id
        self._app       = kw.app
        self._container = kw.container
        self.select     = kw.select
        self.init_state = kw.init_state or {}
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

    def update(self):
        """ in zope this would be __set_state__ -
        we have our state and create the view """
        console.log('update, state:', self.state)
        self.dom_update()

    def ajax(self, meth, send, url):
        self._app.ajax(self, meth, send, url)

    def new_data(self, data):
        console.log('have new data', data)
        self.update()


class ReduxApp:
    id = 'app'
    store = s_store = None
    components_by_id = None

    def __init__(self, init_state):
        self.init_state = init_state or {}
        self.create_store_and_components_registry()
        if self.is_router:
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
        console.log('action', action.type)

        ns = {}             # new state - from old state:
        ns.update(state)
        # and action data:
        d = action.data
        if not d:
            return ns
        for comp_id, kv in d.items():
            comp = self.components_by_id[comp_id]
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
        if self.is_router:
            if not s.route_realized:
                return self.realize_route(self, s.route)

        for id, comp in self.components_by_id.items():
            store_cstate = s[id]
            if comp.__state_id__ != store_cstate._id_:
                data = store_cstate.data
                comp.__state_id__ = store_cstate._id_
                # convenience for the comps: provide a new_data hook ,saves
                # some ifs in the comps:
                if data and comp.state.data != data:
                    comp.state = store_cstate
                    comp.new_data()
                else:
                    comp.state = store_cstate
                    comp.update()


    def register_component(self, comp):
        self.components_by_id[comp.id] = comp
        # here, app may still freely mutate the state, e.g. pull from server:
        # via self.ajax, we have the comp object
        # for now we accept it as is, and this will trigger the comp.update:
        #self.dispatch('comp.init', comp.id, comp.state)


    def ajax(self, comp, meth, send, url):
        def success(data, mode, props):
            id, app = this.comp.id, window.app
            app.dispatch('server_data', id, d(data=data))

        opts = dj(type=meth, url=url,
                dataType='json', data=send,
                success=success, error=success,
                context=dj(comp=comp, app=self))
        jq.ajax(opts)

