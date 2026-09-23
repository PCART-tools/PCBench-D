    def __delitem__(self, key):
        self._warn_deprecated()
        self._cmap_registry.__delitem__(key)
