    def __setitem__(self, key, val):
        self._warn_deprecated()
        self._cmap_registry.__setitem__(key, val)
