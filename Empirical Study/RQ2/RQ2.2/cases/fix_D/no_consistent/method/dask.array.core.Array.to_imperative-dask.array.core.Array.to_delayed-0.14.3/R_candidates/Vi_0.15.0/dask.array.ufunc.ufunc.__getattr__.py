    def __getattr__(self, key):
        if key in self._forward_attrs:
            return getattr(self._ufunc, key)
        raise AttributeError("%r object has no attribute "
                             "%r" % (type(self).__name__, key))
