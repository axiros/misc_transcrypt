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


from tools import d, jd, die, dumps, log

__pragma__('alias', 'jq', '$')
__pragma__('alias', 'lodash', '_')


from redux import LC, ReduxApp, ReduxComponent as RC
from render import PlainStateRenderer as PSR


class App(RC, PSR):
    template = '<div id="top"/>{state}<hr><div id="main">hello world</div>'

class Top(RC, PSR):
    template = 'Top {state}<div id="ts"></div><hr>'

class Comp1(RC, PSR):
    url = '/ch7/server/sample.json'
    template = 'Comp1 {state}<hr><div id="sub"></div>'
    auto_data = 1
    def preregister(self):
        def f():
            self.mount_sub('#sub', 'Comp2', {'new': 'state2'})
        window.setTimeout(f, 2000)

class Comp2(RC, PSR):
    template = 'Comp2 {state}<hr><div id="sub"></div>'

class MyApp(ReduxApp):
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
            "cls": "Top",
            "state": {'idtop': 23}
        }
    }
}

def run(sel):
    app = MyApp()
    app.dispatch('route_update', 'route', route)

    window.app = app
    def f():
        app.foo = 1

        app.dispatch('route_update', 'route',
            {'#mygrid': {
        #        '#new': {'#n2': {'cls': 'Top'}},
                '#top': False,
                '#main':
                    {'#sub': {'cls': 'Top', 'state': {'top': 23}}}}})
    #window.setTimeout(f, 1000)

    def f():
        app.foo = 1

        app.dispatch('route_update', 'route',
            {'#mygrid': {
        #        '#new': {'#n2': {'cls': 'Top'}},
                '#main':
                    {'#sub': {'cls': 'Comp2', 'state': {'new': 'state'}}}}})
    #window.setTimeout(f, 1000)

'''

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



'''
