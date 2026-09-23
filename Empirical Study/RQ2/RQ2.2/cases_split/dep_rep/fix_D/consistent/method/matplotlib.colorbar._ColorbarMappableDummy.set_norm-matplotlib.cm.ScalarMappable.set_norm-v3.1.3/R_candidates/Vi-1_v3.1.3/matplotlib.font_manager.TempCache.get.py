    def get(self, prop):
        key = self.make_rcparams_key()
        if key != self._last_rcParams:
            self._lookup_cache = {}
            self._last_rcParams = key
        return self._lookup_cache.get(prop)
