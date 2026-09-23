    @cache_readonly
    def _data(self):
        return np.arange(self._start, self._stop, self._step, dtype=np.int64)
