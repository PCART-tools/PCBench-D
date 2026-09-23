    def register(self, callback, *args, **kwargs):
        self._callbacks.append((callback, args, kwargs))
