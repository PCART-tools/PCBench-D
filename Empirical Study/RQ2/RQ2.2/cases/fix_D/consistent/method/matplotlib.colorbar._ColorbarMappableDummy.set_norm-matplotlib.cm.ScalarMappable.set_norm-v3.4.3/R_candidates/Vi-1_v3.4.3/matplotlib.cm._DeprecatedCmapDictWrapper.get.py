    def get(self, key, default=None):
        self._warn_deprecated()
        return self._cmap_registry.get(key, default)
