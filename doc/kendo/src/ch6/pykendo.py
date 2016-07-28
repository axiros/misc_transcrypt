import datasource, datepicker, dropdownlist, grid
import themeroller
# TS does currently not expose our imports, so we redeclare, explicitly:
# for clients to be able to call e.g. pykendo.DataSource(...)
class Grid(grid.Grid)                        : pass
class DataSource(datasource.DataSource)      : pass
class DatePicker(datepicker.DatePicker)      : pass
class DropDownList(dropdownlist.DropDownList): pass

# high level widgets
class ThemeRoller(themeroller.ThemeRoller)   : pass


from tools import d, dj

__pragma__('alias', 'jq', '$')
def s_log(x):
    console.log('stream value', x)

def create_redux(reducer, init_state):
    c, k = Redux.createStore, ReduxKefir.observableMiddleware
    c = Redux.applyMiddleware(k)(c)
    wd = window.devToolsExtension
    if wd:
        return c(reducer, init_state, wd())
    else:
        return c(reducer, init_state)

class ReduxApp:
    store = s_store = None
    components_by_id = None
    def __init__(self):
        self.create_store_and_components_registry()

    def create_store_and_components_registry(self):
        self.components_by_id = {}
        initial_state = {}
        self.store = create_redux(self.reducer, initial_state)
        # s_ -> a stream
        self.s_store = ReduxKefir.createProjection(self.store)
        self.s_store.onValue(self.update_components)

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
                cns['__id__'] += 1
                ns[comp_id] = cns
        return ns

    def update_components(self, x):
        s_log(x)
        s = self.store.getState()
        for id, comp in self.components_by_id.items():
            store_cstate = s[id]
            if comp.__state_id__ != store_cstate.__id__:
                data = store_cstate.data
                comp.__state_id__ = store_cstate.__id__
                # convenience for the comps: provide a new_data hook ,saves
                # some ifs in the comps:
                if data and comp.state.data != data:
                    comp.state = store_cstate
                    comp.new_data(data)
                else:
                    comp.state = store_cstate
                    comp.update()


    def register_component(self, comp):
        self.components_by_id[comp.id] = comp
        # here, app may still freely mutate the state, e.g. pull from server:
        # via self.ajax, we have the comp object
        # for now we accept it as is, and this will trigger the comp.update:
        self.dispatch('comp.init', comp.id, comp.state)


    def ajax(self, comp, meth, send, url):
        def success(data, mode, props):
            id, app = this.comp.id, this.app
            app.dispatch('server_data', id, d(data=data))

        opts = dj(type=meth, url=url,
                dataType='json', data=send,
                success=success, error=success,
                context=dj(comp=comp, app=self))
        jq.ajax(opts)


# app = globally available:
app = ReduxApp()
#app.store.dispatch(d(type='test', data=d(foo='bar')))

import time, random
class ReduxComponent:
    ''' A ReduxApp Component with
    - an id
    - serializable primary state
    state can be set by the app, also async.
    '''
    id = state = None
    __state_id__ = 0
    def __init__(self):
        self.register()

    def register(self):
        if not self.id:
            self.id = self.__class__.__name__ + '_' + time.time()
        if not self.state:
            self.state = {}
        # state id, updated at each change. useful for quick diffs in the
        # update_all:
        self.state['__id__'] = self.__state_id__
        app.register_component(self)

    def update(self):
        """ in zope this would be __set_state__ -
        we have our state and create the view """
        console.log('update, state:', self.state)

    def ajax(self, meth, send, url):
        app.ajax(self, meth, send, url)

    def new_data(self, data):
        console.log('have new data', data)





c = ReduxComponent()
c.ajax('get', {}, '/ch6/server/sample.json')




def test_kefir():
    numbers = Kefir.sequentially(100, [1,2,3])
    numbers2 = numbers.map    ( lambda x: x * 2)
    numbers3 = numbers2.filter( lambda x: x != 4)
    numbers3.onValue          ( lambda x: console.log(x))



from tools import d
class NestedDataGrid:
    base_url = None
    def __init__(self, opts, selector):
        self.selector = selector
        self.base_url = opts.base_url
        read = datasource.read(self, self.base_url, self.got_data)
        self.data_source = DataSource(d(read=read))

    def got_data(self, result, mode, opts):
        self.schema = d = result.data.post
        self.type
        # make the datasource happy:
        opts.success(d)


    def error(self, result):
        import pdb; pdb.set_trace()




