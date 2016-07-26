# Integrating JS Frameworks Within Transcrypt

[Chapter One](./ch1_first_widget.md) A First DatePicker Widget

[Chapter Two](./ch2_datasource.md) Kendo Datasource

[Chapter Three](./ch3_server_interaction.md) Server Interaction

[Chapter Four](./ch4_server_interaction_two_way.md) Two Way Server Interaction
(and a theme roller)


## Code Organization

- All the code is within the `src` subfolder.
- Start node's http-server or python -m SimpleHTTPServer there.
- All the kendo assets and jquery plus other libs are in `src/lib`. Any
  libs requiring a commercial license are gitignored. You can download demo
  versions though, fully functional.
- We do not use CDNs since we disable the browser cache during development.
