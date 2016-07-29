#import datasource, datepicker, dropdownlist, grid
#import themeroller
# TS does currently not expose our imports, so we redeclare, explicitly:
# for clients to be able to call e.g. pykendo.DataSource(...)
#class Grid(grid.Grid)                        : pass
#class DataSource(datasource.DataSource)      : pass
#class DatePicker(datepicker.DatePicker)      : pass
#class DropDownList(dropdownlist.DropDownList): pass
#
# high level widgets
#class ThemeRoller(themeroller.ThemeRoller)   : pass


from tools import d, dj, die

__pragma__('alias', 'jq', '$')


from redux import ReduxApp, ReduxComponent as RC
from render import PlainStateRenderer as PSR

class ReduxRouter:
    r_inactive, r_active, r_waiting = 'inact', 'active', 'waiting'
    r_state = 'inact'
    cur_route = None

    def start_router(self):
        pass


    def build_store_id(self, container, comp):
        """
        comp = {comp: 'App', 'state': {...} -> build an id from
        comp. type and principal state """
        if container == self:
            id = [comp.cls]
        else:
            id = [container.id + '.' + comp.cls]
        s = comp.state
        if not s:
            return id[0]
        for k, v in s.items():
            if not k == '_id_':
                id.extend([k, v])
        id =  '.'.join(id)
        return id

    def set_router_state(self, mode):
        console.log('Switching router state to ', mode)
        self.r_state = mode

    def find_class(self, container, cls):
        ''' find the class by string '''
        p = container
        while p:
            c = p[cls]
            if c:
                return c
            p = p._container
        die(cls, 'not found in', container)


    def realize_route(self, container, route):
        console.log('realizing route in', container.id, route, self.r_state)
        for sel, comp in route.items():
            # comp instances are id'ed by their type plus principal state:
            store_id = self.build_store_id(container, comp)
            instance = self.components_by_id[store_id]
            if not instance:
                clsname = comp.cls
                cls = self.find_class(container, clsname)
                m = {}

                instance = cls( id         = store_id,
                                app        = self,
                                select     = sel,
                                init_state = comp.state,
                                container  = container)

                #instance.update()

            __pragma__('js', '{}', 'var need_data = instance.data === null')
            need_data = False
            if instance.url and not 'data' in instance.state:
                self.set_router_state(self.r_waiting)
                need_data = True
                if 'auto_data' in instance and not instance.requesting_data:
                    instance.requesting_data = True
                    instance.get_data()

            if need_data:
                # we dont' go deeper in this one - only when data is there:
                continue
            for k in comp.keys():
                if k in ['cls', 'state']:
                    continue
                self.realize_route(instance, {k: comp[k]})
        if container == self:
            console.log('route complete', route)
            self.route_finished = 1




class App(RC, PSR):
    template = '<div id="top"/>{state}<hr><div id="main">hello world</div>'

class Top(RC, PSR):
    template = 'Top {state}<hr>'

class Comp1(RC, PSR):
    url = '/ch7/server/sample.json'
    template = 'Comp1 {state}<hr><div id="sub"></div>'
    auto_data = 1

class Comp2(RC, PSR):
    template = 'Comp2 {state}<hr><div id="sub"></div>'

class MyApp(ReduxApp, ReduxRouter):
    ''' woraround to get nested classes, not in TS currently '''
    App = App
    Top = Top
    Comp1 = Comp1
    Comp2 = Comp2

route = {
    "#mygrid": {
        "cls": "App",
        "#main": {
            "cls": "Comp1",
            "state": {
            "id1": "bar"
            },
            "#sub": {
            "cls": "Comp2",
            "state": {
                "id2": "foo"
            }
            }
        },
        "#top": {
            "cls": "Top"
        }
    }
}

def run(sel):
    app = MyApp(d(route=route))
    window.app = app





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




