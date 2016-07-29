# Routing


<!-- toc -->

- [Routing](#routing)
	- [Principal State versus Primary State](#principal-state-versus-primary-state)
	- [Async Instantiation](#async-instantiation)
	- [Implementation](#implementation)
		- [Simple Renderer](#simple-renderer)
		- [Router](#router)
			- [Sync Routing](#sync-routing)
				- [Key Achievements](#key-achievements)
		- [Going Async: Data Backed Components - Either / Or. A Valid Assumption ?](#going-async-data-backed-components-either-or-a-valid-assumption)

<!-- tocstop -->


[This](http://jamesknelson.com/simple-routing-redux-react/) is a good read.


Our high level design:

```mermaid
sequenceDiagram
    URLChange-->>RouteAction: E.g. at load, or pasted in
	RouteAction-->>Store: Update
	Store-->>Router: (via observation) calls realize_route()
	note over Router: checks instantiated comps or creates them
    Router-->>CompFoo: instantiates
	CompFoo-->>Server: Async, fetch data
	Server-->>Store: Data, dispatch action
	Store-->>CompFoo: Calls update/new_data
	note over CompFoo: Updates Dom, , sets route_realized flag
	Store-->>Router: realize_route()
	Router-->>CompFooChild: instantiates

```

We see we have to solve a few things:

## Principal State versus Primary State

All primary state must be in Redux, the complete state of the app must be recreatable from it. E.g. the fact that a dropdown list is open after a mouse click means that the open state must be in Redux.

But there are values which are more primary than others: those which the user expects to be set when he enters a route - and those we call principal params, those which are understood in URLs. A dropdown state is normally not principle, while the id of the records displayed within the dropdown options is.

It would be nice to decide via simple adding to a list which params are principle and by simply doing that the routes will be built and understood accordingly.


## Async Instantiation

Say our route parametrizes two nested components. The second one can only be mounted when the first has the data (see kendo detail grid). That means that URL -> Component tree via router can't be done in one syncronous function, but must be step by step with parent components signaling to router that they are ready for it to instantiate the component, deeper in the tree. That does not apply to components which don't need server data though.


Lets do this now:

## Implementation

### Simple Renderer

First we put the redux component related classes into a module and create a little state renderer into the dom, so that we see the updates:

```python
from redux import ReduxApp, ReduxComponent

class PlainStateRenderer:
    """ depends on us being also a Redux Component with state."""
    template = '{state}'
    selector   = None
    _mp  = None
    _rendered_state_id = None # id of last render

    def __repr__(self):
        s = self.__class__.__name__
        if self.selector:
            s += '@' + self.selector
        return s

    def get_html(self):
        html = '<b>' + self.__repr__() + '</b>'
        for k, v in self.state.items():
            html += '<br>   ' + k + ': ' + v
        return html
    html = property(get_html)

    def dom_mount(self):
        self._mp = jq(self.selector)
        self._mp.html(self.template.format({'state': self.html}))

    def dom_update(self):
        ''' re-render after state updates '''
        if self.state._id_ == self._rendered_state_id:
            return

        if not self._mp:
            self.dom_mount()
        else:
            self._mp.html(self.template.format({'state': self.html}))


class MyApp(ReduxApp, PlainStateRenderer):
    template = '{state}<hr><div id="comp1"></div>'


class MyComp(ReduxComponent, PlainStateRenderer):
    pass


def run(sel):
    app = MyApp('#mygrid')
    mc = MyComp('#comp1')
    mc.ajax('get', {}, '/ch7/server/sample.json')
```

<img src="./c7_1.png" width="300"></img>

We can follow the state updates using the debugger. data is already fetched async from the server.

### Router

Now more realistic, using the router. For now we don't care about route parameter serialization into one string with slashes as seperators (see `uniloc.js`) but will deserialize a json structure from the URL, as is. Later we'll invent a clever serialization format.


We would like to have sth like

```python
class App(RC, PSR):
    template = '<div id="top"/>{state}<hr><div id="main">hello world</div>'

class Top(RC, PSR):
    template = 'Top {state}<hr>'

class Comp1(RC, PSR):
    template = 'Comp1 {state}<hr><div id="sub"></div>'

class Comp2(RC, PSR):
    template = 'Comp2 {state}<hr><div id="sub"></div>'

class MyApp(ReduxApp, ReduxRouter):
    ''' woraround to get nested classes, not in TS currently '''
    App = App
    Top = Top
    Comp1 = Comp1
    Comp2 = Comp2

route = {
    "#mygrid": {
        "cls": "App",
        "#main": {
            "cls": "Comp1",
            "state": {
            "id1": "bar"
            },
            "#sub": {
            "cls": "Comp2",
            "state": {
                "id2": "foo"
            }
            }
        },
        "#top": {
            "cls": "Top"
        }
    }
}

def run(sel):
    app = MyApp(d(route=route))
```


have rendered:
1. MyApp
1. Top at app's #top
1. Comp1 at app's #main
1. Comp2 at comp1's #sub

but, as a complication, anticipating that the #sub mountpoint will only be available when Comp1 has the data we want the Comp2 instantiation & mounting only be done once Comp1 has that data.

How do we do that. I think only the component itself can know if the subs can be instantiated in sync (like: app knows that top can be instantiated right away) or if data is missing.

In other words:
The router must instantiate Comp2 only once he 'sees' that Comp1 has its data.


Other example: Top has a dropdown for the user's last emails or alerts. Data to be loaded.

While top may know that e.g. its user session drop down list requires data, it will need to provide a flag to the router that he should go deeper only once data is there.

#### Sync Routing

The sync version of the routing, i.e. when it instantiates the whole tree is pretty much straight forward to do.

<img src="./c7_2.png" width="300"></img>


*Commit hash is 96ae3dd285208531b793c7e317afbb2b39251d30, redux.py and pykendo.py are the interesting modules.*

##### Key Achievements

1. As you can see from the shot we went away from random instance IDs to IDs derived from hirarchy, classname and principal state parameters and their values.
2. We


### Going Async: Data Backed Components - Either / Or. A Valid Assumption ?

Is it valid to assume that a component requires either data, then route realization is only complete once data is there - or it has no data then it can be syncronously completed.

In other words: Isn't it bad design to have components with more than one data backing endpoints on the server? We think yes. E.g. a top bar with a user email dropdown and a general server state dropdown should be designed with two subcomponents which are individually data-backed but not as one big component.


We try that assumption and go with this first Router implementation:

<img src="./c7_3.png" width="300"></img>
*Commit hash is 090b3e5 ('async router'), again redux.py and pykendo.py are the interesting modules and also the renderer.*

- If you try the time slider you'll see that the components neatly mount and unmount into/from the DOM.
- The state of the components remains stored, so no new data fetches when going back, then forward in time, since its the router itself how, when no data is present, triggers the fetch.

This is what we do at store updates:

```python
rs = self.r_state
if rs == self.r_active:
	return
call = 0
if s.action == 'server_data' and rs == self.r_waiting:
	call = 1
if s.route != self.cur_route and rs == self.r_inactive:
	call = 1
if call:
	console.log('calling router')
	self.set_router_state(self.r_active)
	self.realize_route(self, s.route)
	if self.r_state != self.r_waiting:
		self.cur_route = s.route
		self.set_router_state(self.r_inactive)
```
- There are 3 states, inactive, active (in a routing process) and waiting (for server data).
- When we are within a routing process (our router state is active) then we dont' jump in again into realize_route.
- If we have server data and the router is in waiting state we enter it.
- The routing itself (`realize_route`) is always a 100% sync. function, triggering component instantiations and data fetches.