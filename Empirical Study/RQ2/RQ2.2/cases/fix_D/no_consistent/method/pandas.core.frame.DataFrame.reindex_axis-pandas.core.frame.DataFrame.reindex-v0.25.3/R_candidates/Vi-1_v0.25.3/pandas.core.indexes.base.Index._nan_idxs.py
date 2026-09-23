    @cache_readonly
    def _nan_idxs(self):
        if self._can_hold_na:
            w, = self._isnan.nonzero()
            return w
        else:
            return np.array([], dtype=np.int64)
