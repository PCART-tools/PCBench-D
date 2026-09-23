    def __getattr__(self, attr):
        if attr in self._internal_names_set:
            return object.__getattribute__(self, attr)
        if attr in self.obj:
            return self[attr]
        if hasattr(self.obj, attr):
            return self._make_wrapper(attr)

        raise AttributeError(
            "%r object has no attribute %r" % (type(self).__name__, attr)
        )
