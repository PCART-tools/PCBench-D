    @cache_readonly
    def _nan_idxs(self):
        if self._can_hold_na:
            return self._isnan.nonzero()[0]
        else:
            return np.array([], dtype=np.int64)
