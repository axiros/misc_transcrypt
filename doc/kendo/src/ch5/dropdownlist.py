# coding: utf-8
from kendo_base import KendoWidget
__pragma__('alias', 'jq', '$')

class DropDownList(KendoWidget):
    _functions = ['open', 'close', 'value']
    _k_cls = jq().kendoDropDownList.widget

    data_text_field  = 'text'
    data_value_field = 'value'
    data_source      = None
    height           = 500

