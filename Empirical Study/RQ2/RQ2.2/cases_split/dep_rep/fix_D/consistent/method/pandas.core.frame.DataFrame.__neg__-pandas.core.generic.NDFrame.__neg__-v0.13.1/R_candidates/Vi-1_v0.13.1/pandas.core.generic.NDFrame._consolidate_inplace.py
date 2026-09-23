    def _consolidate_inplace(self):
        f = lambda: self._data.consolidate()
        self._data = self._protect_consolidate(f)
