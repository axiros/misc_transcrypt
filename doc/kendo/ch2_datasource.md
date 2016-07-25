# Chapter 2: Kendo DataSource


<!-- toc -->

- [Chapter 2: Kendo DataSource](#chapter-2-kendo-datasource)
	- [Local Data](#local-data)
		- [Rewrite to Python](#rewrite-to-python)
	- [Refactoring Time](#refactoring-time)
			- [DataSource](#datasource)
			- [DatePicker](#datepicker)
			- [KendoComponent, KendoWidget](#kendocomponent-kendowidget)
	- [Wiring the Kendo Callbacks](#wiring-the-kendo-callbacks)

<!-- tocstop -->


This is the central component of kendo to feed widgets with data - from server or from local memory backed information.

Since this is not a widget, kendo will handle it a bit different than e.g. the calendar widget of chapter 1. Lets find out.

## Local Data

We try to get [the official example](http://demos.telerik.com/kendo-ui/datasource/index) to work.

```html
# cat datasource.html
  <!DOCTYPE html>
  <html>
  <head>
      <title></title>
      <link rel="stylesheet" href="lib/kendo.common.min.css" />
      <link rel="stylesheet" href="lib/kendo.default.min.css" /><Paste>
      <script src="lib/jquery.min.js"></script>   
      <script src="lib/kendo.core.js"></script>
      <script src="lib/kendo.data.js"></script>
      <script src="lib/kendo.listview.js"></script>

  </head>
  <body>

                  <table id="movies">
                      <thead>
                          <tr>
                              <th>Rank</th>
                              <th>Rating</th>
                              <th>Title</th>
                              <th>Year</th>
                          </tr>
                      </thead>
                      <tbody>
                          <tr>
                              <td colspan="4"></td>
                          </tr>
                      </tbody>
                  </table>


              <script id="template" type="text/x-kendo-template">
                  <tr>
                      <td>#= rank #</td>
                      <td>#= rating #</td>
                      <td>#= title #</td>
                      <td>#= year #</td>
                  </tr>
              </script>

              <script>
                  $(document).ready(function() {
                      // create a template using the above definition
                      var template = kendo.template($("#template").html());

                      var movies = [
                          { "rank": 1,  "rating": 9.2, "year": 1994, "title": "The Shawshank Redemption" },
                          { "rank": 2,  "rating": 9.2, "year": 1972, "title": "The Godfather" },
                          { "rank": 3,  "rating": 9,   "year": 1974, "title": "The Godfather: Part II" },
                          { "rank": 4,  "rating": 8.9, "year": 1966, "title": "Il buono, il brutto, il cattivo." },
                          { "rank": 5,  "rating": 8.9, "year": 1994, "title": "Pulp Fiction" },
                          { "rank": 6,  "rating": 8.9, "year": 1957, "title": "12 Angry Men" },
                          { "rank": 7,  "rating": 8.9, "year": 1993, "title": "Schindler's List" },
                          { "rank": 8,  "rating": 8.8, "year": 1975, "title": "One Flew Over the Cuckoo's Nest" },
                          { "rank": 9,  "rating": 8.8, "year": 2010, "title": "Inception" },
                          { "rank": 10, "rating": 8.8, "year": 2008, "title": "The Dark Knight" }
                      ];

                      var dataSource = new kendo.data.DataSource({
                          data: movies,
                          change: function() { // subscribe to the CHANGE event of the data source
                              $("#movies tbody").html(kendo.render(template, this.view())); // populate the table
                          }
                      });

                      // read data from the "movies" array
                      dataSource.read();
                  });
              </script>
          </div>


  </body>
  </html>



```
where we just took the concrete non minified kendo libs from [github](https://github.com/telerik/kendo-ui-core/blob/master/src/kendo.data.js), instead of the full kendo.core, since we might want to debug into it. Also we removed some styles, not relevant currently.


Starting the test server and hitting datasource.html gets us the table.


### Rewrite to Python

We boldly change the html to using a Transcrypt DataSource class now:

```js
<script src="__javascript__/datasource.js"></script>
<script>
    $(document).ready(function() {
        var movies = [
            { "rank": 1,  "rating": 9.2, "year": 1994, "title": "The Shawshank Redemption" },
            { "rank": 2,  "rating": 9.2, "year": 1972, "title": "The Godfather" },
            { "rank": 3,  "rating": 9,   "year": 1974, "title": "The Godfather: Part II" },
            { "rank": 4,  "rating": 8.9, "year": 1966, "title": "Il buono, il brutto, il cattivo." },
            { "rank": 5,  "rating": 8.9, "year": 1994, "title": "Pulp Fiction" },
            { "rank": 6,  "rating": 8.9, "year": 1957, "title": "12 Angry Men" },
            { "rank": 7,  "rating": 8.9, "year": 1993, "title": "Schindler's List" },
            { "rank": 8,  "rating": 8.8, "year": 1975, "title": "One Flew Over the Cuckoo's Nest" },
            { "rank": 9,  "rating": 8.8, "year": 2010, "title": "Inception" },
            { "rank": 10, "rating": 8.8, "year": 2008, "title": "The Dark Knight" }
        ];
        var ds = datasource.DataSource( {data: movies});
    });
</script>
</div>
```

We omitted the `change` callback rendering the thing, since that we we'll do in concrete descendents of our pythonic class we are about to create now:

```python
import tools
class DataSource:
    '''
    http://docs.telerik.com/kendo-ui/api/javascript/ui/datepicker#fields-options
    '''
    data = None
    _ds = None
    def __init__(self, opts):
        ''' no mounting we create the datasource right at init '''
        opts = dict(opts)
        # value as date time?
        for k in opts.keys():
            setattr(self, k, opts[k])
        ds = kendo.data.DataSource
        self._ds = __new__(ds(self.opts()))
        debugger

    def opts(self):
        ''' deliver all our non _ params '''
        __pragma__('js', '{}', '''var r = {}''') # want a plain js obj
        for k in dir(self):
            if not k.startswith('_'):
                v = self[k]
                if not tools.jstype(v, 'function'):
                    r[k] = v
        return r
```

recycling from the lessons learnt in chapter 1:
1. the dict wrapper
1. "auto js opts from class/object vars" function
1. our knowledge about `__new__` of Transcrypt.

In the console, at the breakpoint we can do now `ds.read()` and `ds.data()` delivers the data.

Splendid.


## Refactoring Time

So we think we understood that there are two sorts of components in kendo: One which mount to the DOM the others which are data only.
They handle pretty much the same, regarding config, functions and callbacks.

So, lets refactor the common stuff, including datasource and datepicker within one html to be able to test the refactoring results.

We'll expose all widgets via a new module, `pykendo.py`:

```python
import datasource, datepicker
# TS does currently not expose our imports, so we redeclare, explicitly:
# for clients to be able to call e.g. pykendo.DataSource(...)
class DataSource(datasource.DataSource): pass
class DatePicker(datepicker.DatePicker): pass
```

use in the HTML pretty much unchanged, e.g.:

```js
$ (document).ready(function() {                                       
        var d    = pykendo.DatePicker                                     
        var time = d._mod_time.time                                       
        var o = {'ts': time()-2 * 86400}                                  
        d(o, '#pydatepicker')                         
}
```

with these nice and clean component modules:


#### DataSource

with only the function as above:

```python
~/ch2 $ cat datasource.py
from kendo_base import KendoComponent

class DataSource(KendoComponent):
    _k_cls = kendo.data.DataSource
    data = None
```

#### DatePicker

```python
~/ch2 $ cat datepicker.py
import tools
from kendo_base import KendoWidget
__pragma__('alias', 'jq', '$')

class DatePicker(KendoWidget, tools.PyDate):
    '''
    vim: gx over the url to open in browser:
    http://docs.telerik.com/kendo-ui/api/javascript/ui/datepicker#fields-options
    '''
    format = 'yyyy-MM-dd'
    _k_cls = jq().kendoDatePicker.widget
    _functions = ['enable', 'close', 'destroy', 'readonly', 'max', 'min',
                  'open', 'setOptions']


    def post_init(self):
        self.set_value(self.ts)
```

and

#### KendoComponent, KendoWidget

```python
$ cat kendo_base.py

import tools
class KendoComponent:
    _k_cls, _k_obj = None, None # the kendo component and instance
    # containing direct callable functions, e.g. open on a datepicker:
    # to be set by a descendant
    _functions = None

    def __init__(self, opts):
        opts = dict(opts)
        for k in opts.keys():
            setattr(self, k, opts[k])
        self.post_init()
        if not self.mount:
            self.instantiate()

    def post_init(self):
        """ customization hook"""
        pass

    def instantiate(self):
        # instantiation of dom-less components:
        if self._jqel:
            self._k_obj = __new__(self._k_cls(self._jqel, self.opts()))
        else:
            self._k_obj = __new__(self._k_cls(self.opts()))

        if self._functions:
            # setting the functions into our selfes, take care of 'this' in the
            # funcs:
            for k in self._functions:
                setattr(self, k, getattr(self._k_obj, k).bind(self._k_obj))
        return self

    def opts(self):
        ''' deliver all our non _ params '''
        __pragma__('js', '{}', '''var jsopts = {}''') # want a plain js obj
        for k in dir(self):
            if not k.startswith('_'):
                v = self[k]
                if not tools.jstype(v, 'function'):
                    jsopts[k] = v
        return jsopts


__pragma__('alias', 'jq', '$')
class KendoWidget(KendoComponent):
    _jqel      = None # the jquery wrapper where we are mounted
    def __init__(self, opts, selector):
        KendoComponent.__init__(self, opts)
        if selector:
            self.mount(selector)

    def mount(self, selector):
        jels = jq(selector)
        if len(jels) != 1:
            raise Exception("You have 0 or more than one match on the selector")
        self._jqel = jels[0]
        return self.instantiate()

```

The two ifs in the base instead of super class calling we find ok if its just 2 principal cases. But thats a personal style question.

Important is that everything worked as expected and we think we are getting pretty effective with this all...


## Wiring the Kendo Callbacks


Into the `def opts` wrapper we add a universal callback mapper, since we see those are sent into kendo like this:

```
{'change': <callback function>}
```

so we can populate that, based on a the presence of e.g. a `def on_change` function in our concrete descendents.

Looks then like this:

We derive from our DataSource, with a concreate on_change handler, for now in `pykendo.py` (will later be in sth like `myapp.py` ):

```python
__pragma__('alias', 'jq', '$')
class MyDataSource(DataSource):
    def on_change(self):
        template = kendo.template(jq("#template").html());
        jq("#movies tbody").html(kendo.render(template, self._k_obj.view()));
```

then add to our DataSource:

```python
_functions = ['read']
def __init__(self, opts):
    KendoComponent.__init__(self, opts)
    self.read()
```

and in our `def opts` wrapper:

```python
if not tools.jstype(v, 'function'):
    jsopts[k] = v
else:
    if k.startswith('on_'):
        jsopts[k[3:]] = v
```


and call MyDataSource in html like `var ds = pykendo.MyDataSource( {data: movies});`

and bum - it just works, we get the table. Total productivity flash :-)
