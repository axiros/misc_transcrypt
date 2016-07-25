# Chapter 3: DataSource Server Interaction

Lets hook up the datasource with data from a server.

## Fake JSON server

We create a fake server and start it:

```markdown
# json server


## Installation

You need nodejs and npm. Then:

    npm install -g json-server


## Usage

    json-server --watch db.json
    and e.g. GET http://localhost:3000/posts/1

See https://github.com/typicode/json-server for further examples.
```

So, we take our movies list from the html into db.json and start the server:

```json
~/demo/ch3/server $ cat db.json
{"movies": [
    { "rank": 1,  "rating": 9.2, "year": 1994, "title": "The Shawshank Redemption" },
    { "rank": 2,  "rating": 9.2, "year": 1972, "title": "The Godfather" },
    { "rank": 3,  "rating": 9,   "year": 1974, "title": "The Godfather: Part II" },
    { "rank": 4,  "rating": 8.9, "year": 1966, "title": "Il buono, il brutto, il cattivo." },
    { "rank": 5,  "rating": 8.9, "year": 1994, "title": "Pulp Fiction" },
    { "rank": 6,  "rating": 8.9, "year": 1957, "title": "12 Angry Men" },
    { "rank": 7,  "rating": 8.8, "year": 1975, "title": "One Flew Over the Cuckoo's Nest" },
    { "rank": 8,  "rating": 8.8, "year": 2010, "title": "Inception" },
    { "rank": 9,  "rating": 8.2, "year": 2008, "title": "The Dark Knight" }
]}
~/demo/ch3/server $ json-server --watch db.json
```
and `~/demo/ch3 $ wget http://127.0.0.1:3000/movies -O -` delivers them.

In the html we remove the data parameter: `var ds = pykendo.MyDataSource();` and get the interaction up in `pykendo.MyDataSource`.

[This](http://demos.telerik.com/kendo-ui/datasource/remote-data-binding) is the blueprint.

So:

```python
__pragma__('alias', 'jq', '$')
class MyDataSource(DataSource):
    def __init__(self, opts):
        self.transport = {
                'read': {
                    'url': 'http://127.0.0.1:3000/movies',
                    'dataType': 'jsonp'
                    }}
        DataSource.__init__(self, opts)

    def on_change(self):
        template = kendo.template(jq("#template").html());
        jq("#movies tbody").html(kendo.render(template, self._k_obj.view()));
```

Reload the browser - and we see on the json server:

```
GET /movies?callback=jQuery1123011691446590675514_1469457283503&_=1469457283504 200 1.541 ms - 981
```
(kendos way of getting callbacks assigned to potentially concurrent requests)

And we have the data - as before with the local table.

Fun.

### Refactor

Lets refactor the obvious, we want `url` or full `transport` dict as a parameter.

We remove `__init__` again from MyDataSource and do:

```python
var ds = pykendo.MyDataSource({url:'http://127.0.0.1:3000/movies'})

~/demo/ch3 $ cat datasource.py
from kendo_base import KendoComponent

class DataSource(KendoComponent):
    '''
    http://docs.telerik.com/kendo-ui/api/javascript/ui/datepicker#fields-options
    '''
    _k_cls = kendo.data.DataSource
    data = None
    transport = None
    _functions = ['read']
    def __init__(self, opts):
        od = dict(opts)
        url = od.pop('url', None)
        if url:
            od['transport'] = {'read': {'url': url, 'dataType': 'jsonp'}}
        KendoComponent.__init__(self, opts)
        self.read()
```

done, works, MyDataSource has a `.transport` dict, `on_change` callback still working.

*Note how the opts was wrapped intermediately into a transcrypt dict to use the pop function, while still based on the original mutable js opts object.*
