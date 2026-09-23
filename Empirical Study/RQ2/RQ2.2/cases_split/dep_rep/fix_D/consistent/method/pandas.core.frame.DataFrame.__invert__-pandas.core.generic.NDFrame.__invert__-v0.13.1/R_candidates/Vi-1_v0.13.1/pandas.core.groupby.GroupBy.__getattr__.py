    def __getattr__(self, attr):
        if attr in self.obj:
            return self[attr]

        if hasattr(self.obj, attr) and attr != '_cache':
            return self._make_wrapper(attr)

        raise AttributeError("%r object has no attribute %r" %
                             (type(self).__name__, attr))
