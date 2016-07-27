# coding: utf-8
import tools
from dropdownlist import DropDownList


class ThemeRoller(DropDownList):
    """ based one http://jsfiddle.net/gyoshev/Gxpfy/"""
    data_text_field  = "name"
    data_value_field = "value"
    height           = 500
    data_source = tools.name_value_pairs([
       [ "Black"        , "black"         ],
       [ "MaterialBlack", "materialblack" ],
       [ "MetroBlack"   , "metroblack"    ],
       [ "Office365"    , "office365"     ],
       [ "Uniform"      , "uniform"       ],
       [ "Nova"         , "nova"          ],
       [ "Moonlight"    , "moonlight"     ],
       [ "Meego"        , "meego"         ],
       [ "Material"     , "material"      ],
       [ "HighContrast" , "highcontrast"  ],
       [ "Flat"         , "flat"          ],
       [ "Fiori"        , "fiori"         ],
       [ "Bootstrap"    , "bootstrap"     ],
       [ "Blue Opal"    , "blueopal"      ],
       [ "Default"      , "default"       ],
       [ "Metro"        , "metro"         ],
       [ "Silver"       , "silver"        ]])

    def on_change(self, e):
        theme = self.value() or 'default'
        self.change_theme(theme)

    def change_theme(self, theme):
        __pragma__('js', '{}', '''
    var body_bg = {'moonlight'    : '#414550',
                   'metroblack'   : 'black',
                   'materialblack': '#363636' }

    var doc = document,
        kendoLinks = $("link[href*='kendo.']", doc.getElementsByTagName("head")[0]),
        commonLink = kendoLinks.filter("[href*='kendo.common']"),
        skinLink = kendoLinks.filter(":not([href*='kendo.common'])"),
        href = location.href,
        skinRegex = /kendo\.\w+(\.min)?\.css/i,
        extension = skinLink.attr("rel") === "stylesheet" ? ".css" : ".less",
        url = commonLink.attr("href").replace(skinRegex, "kendo." + theme + "$1" + extension),
        exampleElement = $("#example");

    function replaceTheme() {
        var oldSkinName = $(doc).data("kendoSkin"),
            newLink;

        //if ($.browser.msie) {
        //    newLink = doc.createStyleSheet(url);
        //} else {
            newLink = skinLink.eq(0).clone().attr("href", url);
        //}

        newLink.insertBefore(skinLink[0]);
        skinLink.remove();

        $(doc.documentElement).removeClass("k-" + oldSkinName).addClass("k-" + theme);
        // rework Site.css:
        var bg = '#fff'
        var bg2 = '#eee'
        if (theme.indexOf('black') > -1 ||
            theme.indexOf('contrast') > -1 ||
            theme.indexOf('moonlight') > -1
            ) {
            bg = '#222';
            bg2 = '#777';
            }

        var body = body_bg[theme] || '#fff'
        $('body').css({'background-color': body})
        // styles of dashboards:
        $('.section-white'      ).css({'background-color': bg})
        $('#main-section-header').css({'background-color': bg})
        $('#main-section'       ).css({'background-color': bg2})
    }

    replaceTheme();
    ''')

