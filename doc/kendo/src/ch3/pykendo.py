import datasource, datepicker
# TS does currently not expose our imports, so we redeclare, explicitly:
# for clients to be able to call e.g. pykendo.DataSource(...)
class DataSource(datasource.DataSource): pass
class DatePicker(datepicker.DatePicker): pass

__pragma__('alias', 'jq', '$')
class MyDataSource(DataSource):
    def on_change(self):
        template = kendo.template(jq("#template").html());
        jq("#movies tbody").html(kendo.render(template, self._k_obj.view()));

