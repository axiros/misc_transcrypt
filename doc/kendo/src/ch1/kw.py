__pragma__ ('alias', 'S', '$')
from observable import Observable

class PyWin:
    width = '200px'

class Window(Observable, kendo.ui.Window):
    widget = None

    def __init__(self, parent):
        self.parent = parent


        __pragma__('js', '{}', '''

(function ($) {
    var ui = kendo.ui,
        Window = ui.Window,
        KWINDOWCONTENT = ".k-window-content";

    var MyWindow = Window.extend({
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
            name: 'MyWindow'
        },

        _customize: function () {
            this.originalValue = $(this.element).css('color');
            $(this.element).css('color', 'green');
        },

        _destroyCustomize: function () {
            $(this.element).css('color', this.originalValue);
        }
    });

    ui.plugin(MyWindow);

 /**
    * update kendoWindow's _object method to return our new widget as well
    */
    ui.Window.fn._object = function (element) {
        var content = element.children(KWINDOWCONTENT);

        return content.data("kendoWindow") || content.data("kendoMyWindow") || content.data("kendo" + this.options.name);
    };
})(jQuery);



        ''')



        __pragma__('js', '{}', '''
     (function ($) {
        var CustomListView = kendo.ui.ListView.extend({
          options: {
              name: "CustomListView"
          },
          say: function(message) {
              console.log(message); 
          }
        });
        kendo.ui.plugin(CustomListView);
      })(jQuery);
    $("#app2").kendoCustomListView({
            dataSource: new kendo.data.DataSource({
                data: [
                { name: "Name 1" },
                { name: "Name 2" },
                { name: "Name 3" }
                ]
            }),
          template: "<div>#= name #</div>"
        });

        //call widget method (please watch the console)
        $("#app2").data("kendoCustomListView").say("hello");
    ''')

        __pragma__('js', '{}', '''

                    var myWindow = $("#app"),
                        undo = $("#undo");

                    undo.click(function() {
                        myWindow.data("kendoWindow").open();
                        undo.fadeOut();
                    });

                    function onClose() {
                        undo.fadeIn();
                    }
                    myWindow.kendoMyWindow({
                        width: "600px",
                        title: "About Alvar Aalto",
                        visible: false,
                        actions: [
                            "Pin",
                            "Minimize",
                            "Maximize",
                            "Close"
                        ],
                        close: onClose
                    }).data("kendoMyWindow").center().open();
                    ''')

