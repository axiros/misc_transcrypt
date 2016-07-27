# Integrating JS Frameworks Within Transcrypt

[Chapter One](./ch1_first_widget.md) A First DatePicker Widget

[Chapter Two](./ch2_datasource.md) Kendo Datasource

[Chapter Three](./ch3_server_interaction.md) Server Interaction

[Chapter Four](./ch4_server_interaction_two_way.md) Two Way Server Interaction
(and a theme roller)

## Commerical Code

In chapter 4 we are switching from the open source version of KendoUI to a commercial one, integrating its data grid. Why? Because in my company this is currently being used and we are piling up chunks of badly maintainable javascript to customize it. Thats why I integrate it within Transcrypt and the documentation of the journey may help you integrating other, similar tools from the js world.

You can follow the tutorial by downloading a trial version which is free of charge.

> I would be glad to get a note if someone integrates e.g. [`aggrid`](https://www.ag-grid.com/) or even [`OpenUI5`](https://openui5.hana.ondemand.com/#docs/api/symbols/sap.ui.layout.form.GridLayout.html) into Transcrypt. Both are equally great, if not better - plus free.



## Code Organization

- All the code is within the `src` subfolder.
- Start node's http-server or python -m SimpleHTTPServer there.
- All the kendo assets and jquery plus other libs are in `src/lib`. Any
  libs requiring a commercial license are gitignored. You can download demo
  versions though, fully functional.
- We do not use CDNs since we disable the browser cache during development.
