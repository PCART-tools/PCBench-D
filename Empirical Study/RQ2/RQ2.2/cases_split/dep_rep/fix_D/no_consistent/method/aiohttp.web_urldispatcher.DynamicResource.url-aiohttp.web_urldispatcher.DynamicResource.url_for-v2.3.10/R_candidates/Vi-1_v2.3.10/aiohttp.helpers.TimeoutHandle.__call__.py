    def __call__(self):
        for cb, args, kwargs in self._callbacks:
            try:
                cb(*args, **kwargs)
            except:
                pass

        self._callbacks.clear()
