from kendo_base import KendoComponent
# test urls
get_list = 'http://127.0.0.1:3000/posts/'


class DataSource(KendoComponent):
    '''
    http://docs.telerik.com/kendo-ui/api/javascript/ui/datepicker#fields-options
    '''
    _k_cls = kendo.data.DataSource
    data = None
    _functions = ['read']
    def __init__(self, opts):
        KendoComponent.__init__(self, opts)
        self.read()

