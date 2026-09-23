    @cache_readonly
    def _nan_idxs(self):
        w, = self._isnan.nonzero()
        return w
