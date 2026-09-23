    def __getitem__(self, key):
        self._warn_deprecated()
        return self._cmap_registry.__getitem__(key)
