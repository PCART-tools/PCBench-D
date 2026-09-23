    def __iter__(self):
        self._warn_deprecated()
        return self._cmap_registry.__iter__()
