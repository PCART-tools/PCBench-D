    def set(self, prop, value):
        key = self.make_rcparams_key()
        if key != self._last_rcParams:
            self._lookup_cache = {}
            self._last_rcParams = key
        self._lookup_cache[prop] = value
