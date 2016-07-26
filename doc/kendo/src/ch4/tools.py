import time

def name_value_pairs(l):
    ret = []
    for k, v in l:
        ret.append({'name': k, 'value': v})
    return ret


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
