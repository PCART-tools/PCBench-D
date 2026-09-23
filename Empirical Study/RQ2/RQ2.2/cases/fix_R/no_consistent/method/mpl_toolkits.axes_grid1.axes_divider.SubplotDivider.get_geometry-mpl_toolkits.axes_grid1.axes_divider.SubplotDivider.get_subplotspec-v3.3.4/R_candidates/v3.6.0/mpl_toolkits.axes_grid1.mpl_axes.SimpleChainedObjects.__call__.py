    def __call__(self, *args, **kwargs):
        for m in self._objects:
            m(*args, **kwargs)
