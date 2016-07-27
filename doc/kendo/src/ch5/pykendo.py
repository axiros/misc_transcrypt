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




