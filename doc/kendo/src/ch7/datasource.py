from kendo_base import KendoComponent
from tools import d
# test urls
get_list = 'http://127.0.0.1:3000/posts/'

__pragma__('alias', 'jq', '$')

def read(cb_handler, url, success, error):
    success = success or cb_handler.success
    error   = error or cb_handler.error
    def ajax():
        opts =d(type='get', dataType='json', data=d(), url=url,
                success=success, error=error)
        return jq.ajax(opts)
    return lambda: ajax()


class DataSource(KendoComponent):
    '''
    http://docs.telerik.com/kendo-ui/api/javascript/ui/datepicker#fields-options
    '''
    _k_cls = kendo.data.DataSource
    data = None
    page_size = 20
    url = None
    _data_type = 'json'

    transport = None
    _functions = ['read']
    def __init__(self, opts):
        if opts == undefined:
            opts = {}
        od = dict(opts)
        KendoComponent.__init__(self, opts)
        self.read()

    def post_init(self):
        ''' lets see what we got from the caller '''
        if self.data or self.tranport:
            return
        self.transport = t = {}
        if self.read:
            t['read'] = self.read
        elif self.url:
            t['read'] = d(url=self.url, dataType=self._data_type)

    def on_change(self, *a):
        print('data changed')


