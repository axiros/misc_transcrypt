import time

def die(err_type, *a):
    p = ['!!']
    for obj in a:
        if obj.__repr__:
            p.append(obj.__repr__())
        else:
            p.append(obj)
    console.log.apply(console, p)
    throw (__new__( Error(err_type)))


def decorate(cls, func, dfunc):
    """
    class : a Transcrypt class
    func  : name of method to decorate
    dfunc : decorator function

    Example:
        e.g. dfunc =
            def mydeco(obj, func, *a): return func(obj, *a)
        class A:
            i = 2
            def foo(self, j, k): return self.i * int(j) * int(k)

        decorate(A, 'foo', dfunc)
        A().foo(4, 5) -> will pass the args and the result through the mydeco

    """
    def d3(*a):
        # stage 3: call the decorator like known in python (obj, func, args):
        return this['dfunc'](this['self'], this['orig'], *a)
    def d2(f, dfunc):
        # stage2: return stage3 function, with context
        return lambda: d3.bind({'self': this, 'orig': f, 'dfunc': dfunc})
    # stage1: define the getter, func = name of original function:
    cls.__defineGetter__(func, d2(cls[func], dfunc))

def d(*a):
    ''''
    deep = d(foo=d(bar=42)) => deep = {'foo': {'bar': 42}}
    with the map a pure js obj.
    '''
    r = a[0]
    if not r:
        __pragma__('js', '{}', 'return {}')
    del r['constructor']
    del r['__class__']
    return r


def name_value_pairs(l):
    return [{'name': k, 'value': v} for k, v in l]


def camelize(s):
    ''' kendo wants camelCase, we want snake_case '''
    s = s.split('_')
    r = s[0]
    for part in s[1:]:
        r += part.capitalize()
    return r



def jstype(obj, typ):
   __pragma__('js', '{}', '''
   var t = typeof(obj)''')
   if t == typ:
       return True
   return False

class PyDate:
    '''
    Descendants get a self.value property, which is always in sync
    with an internal self.ts = unixtime'''
    _value = ts = None
    _mod_time = time
    def get_value(self):
        ''' the js Date we return is based on the unixtime ts '''
        if self._value:
            t = self._value.getTime() / 1000
            if t == self.ts:
                return self._value
        # will set the new self._value to self.ts and return it
        return self.set_value()

    def set_value(self, ts):
        ''' accept none, js data and unix time
        on none our self.ts wins
        '''
        if ts:
            if not jstype(ts, 'number'):
                self._value = ts
                self.ts = ts.getTime() / 1000
                return self._value
            # ts = unixtime:
            self.ts = ts
            self._value = __new__(Date(ts * 1000))
            return self._value
        if not self.ts:
            self.ts = time.time()
        return self.set_value(self.ts)

    value = property(get_value, set_value)
