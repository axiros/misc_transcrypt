class Observable:
    observers = None
    def handlers(self, ev):
        # initting observers and even handlers implicitelly
        obs = self.observers
        if obs == None:
            self.observers = obs = {}
        handlers = obs[ev] # no setdefault :-/
        if not handlers:
            obs[ev] = handlers = []
        return handlers

    def register_handler(self, mode, ev, handler):
        h = self.handlers(ev)
        if mode == 'on' and not handler in h:
            h.append(handler)
        elif mode == 'off' and handler in h:
            h.remove(handler)

    def on(self, ev, handler):
        return self.register_handler('on', ev, handler)

    def off(self, ev, handler):
        return self.register_handler('off', ev, handler)

    def fire(self, ev, nfos):
        # ev just a string, nfos arbitrary or undef
        h = self.handlers(ev)
        for handler in h:
            handler([ev, self, nfos])


