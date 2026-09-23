    def remove_callback(self, func, *args, **kwargs):
        '''
        Remove `func` from list of callbacks. `args` and `kwargs` are optional
        and used to distinguish between copies of the same function registered
        to be called with different arguments.
        '''
        if args or kwargs:
            self.callbacks.remove((func, args, kwargs))
        else:
            funcs = [c[0] for c in self.callbacks]
            if func in funcs:
                self.callbacks.pop(funcs.index(func))
