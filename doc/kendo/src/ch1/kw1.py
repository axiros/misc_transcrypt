# vim: ft=python
__pragma__ ('alias', 'S', '$')
from observable import Observable

ui = kendo.ui
KWINDOWCONTENT = ".k-window-content"

class PyWin:
    width = '600px'

class W(PyWin, kendo.ui.Window):
    options = {'name': 'MyWindow'}
    def init(self, element, options):
        debugger
        self.fn.init.call(self, element, options)

__pragma__('js', '{}', '''

(function ($) {
    var ui = kendo.ui,
        Window = ui.Window,
        KWINDOWCONTENT = ".k-window-content";

    var My1Window = Window.extend({
        init: function (element, options) {
            var that = this;

            Window.fn.init.call(that, element, options);
            that._customize();
        },
        destroy: function () {
            var that = this;

            that._destroyCustomize();
            Window.fn.destroy.call(that);
        },

        options: {
            name: 'My1Window'
        },

        _customize: function () {
            this.originalValue = $(this.element).css('color');
            $(this.element).css('color', 'green');
        },

        _destroyCustomize: function () {
            $(this.element).css('color', this.originalValue);
        }
    });

    ui.plugin(My1Window);

 /**
    * update kendoWindow's _object method to return our new widget as well
    */
    ui.Window.fn._object = function (element) {
        var content = element.children(KWINDOWCONTENT);

        return content.data("kendoWindow") || content.data("kendoMy1Window") || content
    };
})(jQuery);



        ''')


w = W()
__pragma__('js', '{}', '''

var a = function () {
    var MyWindow = ui.Window.extend(w)

    ui.plugin(MyWindow);

    ui.Window.fn._object = function (element) {
        var content = element.children(KWINDOWCONTENT);

    return content.data("kendoWindow") || content.data("kendoMyWindow") || content.data("kendo" + this.options.name);
    };
}

a()


        ''')

class A1:
    def __init__(self):
        self.a = 'foo'

    def __call__(self):
        return self.a


b = A1()
c = b.__call__()

class Window(Observable, kendo.ui.Window):
    widget = None

    def __init__(self, parent):
        self.parent = parent

        __pragma__('js', '{}', '''
                    $('#app').kendoMyWindow({
                        title: "About Alvar Aalto",
                        visible: false,
                        actions: [
                            "Pin",
                            "Minimize",
                            "Maximize",
                            "Close"
                        ],
                    }).data("kendoMyWindow").center().open();
                    ''')

