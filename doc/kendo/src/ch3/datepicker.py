import tools
from kendo_base import KendoWidget
__pragma__('alias', 'jq', '$')

class DatePicker(KendoWidget, tools.PyDate):
    '''
    vim: gx over the url:
    http://docs.telerik.com/kendo-ui/api/javascript/ui/datepicker#fields-options
    '''
    format = 'yyyy-MM-dd'
    _k_cls = jq().kendoDatePicker.widget
    _functions = ['enable', 'close', 'destroy', 'readonly', 'max', 'min',
                  'open', 'setOptions']


    def post_init(self):
        self.set_value(self.ts)

