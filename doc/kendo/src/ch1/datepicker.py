import time, tools
__pragma__('alias', 'jq', '$')

class DatePicker(tools.PyDate):
    '''
    vim: gx over the url:
    http://docs.telerik.com/kendo-ui/api/javascript/ui/datepicker#fields-options
    '''
    _mod_time = time # ref for plain js
    _widget    = None
    _jqel      = None
    format = 'yyyy-MM-dd'

    def __init__(self, opts, selector):
        opts = dict(opts)
        # value as date time?
        for k in opts.keys():
            setattr(self, k, opts[k])
        self.set_value(self.ts)
        if selector:
            self.mount(selector)

    def opts(self):
        ''' deliver all our non _ params '''
        __pragma__('js', '{}', '''var r = {}''') # want a plain js obj
        for k in dir(self):
            if not k.startswith('_'):
                v = self[k]
                if not tools.jstype(v, 'function'):
                    r[k] = v
        return r

    def mount(self, el):
        jels = jq(el)
        self._widget_cls = jq().kendoDatePicker.widget
        for jel in jels:
            self._jqel = jel
            if self._widget:
                raise Exception("You have more than one match on the selector")
            self._widget = __new__(self._widget_cls(jel, self.opts()))
        # setting the functions into our selfes, take care of 'this' in the
        # funcs:
        for k in ('enable', 'close', 'destroy', 'readonly', 'max', 'min',
                  'open', 'setOptions'):
            setattr(self, k, getattr(self._widget, k).bind(self._widget))
        return self

