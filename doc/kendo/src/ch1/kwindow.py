# vim: ft=python
__pragma__ ('alias', 'S', '$')
from observable import Observable

class Py: pass
class DS(kendo.data.DataSource, Py):
    def __init__(self, data):
        data = data.data or data # depends on if we are called with data= or not
        self.options = {'data': data}
        self.prototype = kendo.data.DataSource.prototype
        self.prototype.init(self.options)
ds = DS([{'name': 'v1'}, {'name': 'asdfadf'}])


class LV:
    def __init__(self):
        self.options = {'name': 'CustomListView'}
        self.options['fo'] = 2

    def say(self, msg):
        console.log(msg, self.options)

    def __call__(*a):
        debugger;

lv = LV()
CustomListView = kendo.ui.ListView.extend(lv)
kendo.ui.plugin(CustomListView)
ds = { 'dataSource': ds,
       'template': "<div>NAME #= name #</div>"
     }
el1 = S('#app')
el1.kendoCustomListView(ds)

#S("#app").data("kendoCustomListView").say("hello there")




def f(n, self, a):
    debugger
    res = n.prototype.init(a[0][0], a[1])
class MyListView(kendo.ui.ListView, Py):
    def __init__(self):
        self.dataSource = ds
        self.template =  "<div>ASDFNAME #= name #</div>"
        self.options = {'name': 'MyListView', 'datasource': ds}
        #n = kendo.ui.ListView.extend(self)
        #n2 = kendo.ui.plugin(n)
        el = S('#app2')
        a = [el, self.options]
        f(kendo.ui.ListView, self, a)
        #self.prototype = kendo.ui.ListView.prototype
        #self.prototype.init(el, self.options)

ds = MyListView()
#kendo.ui.plugin(ds)
el = S('#app2')

el.kendoListView(ds)












#ds2 = kendo.data.DataSource.extend(DS([{'name': 'vasdf2'}, {'name': 'aasdfsdfadf'}]))

#S('#app2').kendoCustomListView({
#          'dataSource': ds2,
#          'template': "<div>NAME #= name #</div>"
#        });

class Window: pass
