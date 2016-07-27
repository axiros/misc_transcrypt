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



from tools import d
class MyGridDataSource(DataSource):
    #type = 'jsonp'
    url = "http://localhost:3000/movies"
    schema = d(model=d(
                id='rank',
                fields=d(
                    rank   = d(type='number')
                   ,rating = d(type='number')
                   ,year   = d(type='number')
                   ,title  = d(type='string'))))


class MyGrid(Grid):
    data_source = MyGridDataSource()
    height = 550
    sortable = groupable = filterable = True
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


