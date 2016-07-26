def debug(obj, func, *a):
    console.log('before call', a)
    res = func(obj, *a)
    console.log('after call, got', res)
    return res


def decorate(cls, func, dfunc):
    """
    class : a Transcrypt class
    func  : name of method to decorate
    dfunc : decorator function

    Example:
        e.g. def mydeco(obj, func, *a): return func(obj, *a)
    """
    def d3(*a):
        # stage 3: call the decorator like known in python (obj, func, args):
        return this['dfunc'](this['self'], this['orig'], *a)
    def d2(f, dfunc):
        # stage2: return stage3 function, with context
        return lambda: d3.bind({'self': this, 'orig': f, 'dfunc': dfunc})
    # stage1: define the getter, func = name of original function:
    cls.__defineGetter__(func, d2(cls[func], dfunc))

class A:
    i = 2
    def foo(self, bar, baz):
        return int(bar) * int(baz) * self.i

console.log(A().foo(1, 2))

decorate(A, 'foo', debug)

a = A()
console.log(a.foo(3, 2))


debugger



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

__pragma__('alias', 'jq', '$')
class MyDataSource(DataSource):
    def on_change(self):
        template = kendo.template(jq("#template").html());
        jq("#movies tbody").html(kendo.render(template, self._k_obj.view()));


class MyGridDataSource(DataSource):
    #type = 'jsonp'
    url = "http://localhost:3000/movies"

class MyGrid(Grid):
    data_source = MyGridDataSource()
    height = 550
    sortable = groupable = True
    pageable = {'refresh': True, 'pageSizes': True, 'buttonCount': 5}
    columns = [{'field': "rank",
                'title': "Rank",
                }, {
                'field': "rating",
                'title': "Rating"
                }, {
                'field': "year",
                'title': "Year"
                }, {
                'field': "title",
                'title': "Title",
                'width': 150
                }]


