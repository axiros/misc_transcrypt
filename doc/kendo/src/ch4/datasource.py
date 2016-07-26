from kendo_base import KendoComponent
# test urls
get_list = 'http://127.0.0.1:3000/posts/'


class DataSource(KendoComponent):
    '''
    http://docs.telerik.com/kendo-ui/api/javascript/ui/datepicker#fields-options
    '''
    _k_cls = kendo.data.DataSource
    data = None
    page_size = 20
    url = None
    _data_type = 'jsonp'

    transport = None
    _functions = ['read']
    def __init__(self, opts):
        if opts == undefined:
            opts = {}
        od = dict(opts)
        url = od.pop('url', self.url)
        transport = od['transport'] or self.transport
        if not transport:
            od['transport'] = {
                    'read': {
                        'url': url,
                        'dataType': self._data_type}}
        KendoComponent.__init__(self, opts)
        self.read()

