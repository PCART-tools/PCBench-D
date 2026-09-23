    def add_callback(self, func, *args, **kwargs):
        '''
        Register `func` to be called by timer when the event fires. Any
        additional arguments provided will be passed to `func`.
        '''
        self.callbacks.append((func, args, kwargs))
