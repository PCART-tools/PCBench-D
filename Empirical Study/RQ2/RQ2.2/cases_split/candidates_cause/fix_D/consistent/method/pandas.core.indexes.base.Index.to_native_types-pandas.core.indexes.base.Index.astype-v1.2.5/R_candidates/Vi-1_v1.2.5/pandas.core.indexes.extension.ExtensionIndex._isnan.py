    @cache_readonly
    def _isnan(self) -> np.ndarray:
        return self._data.isna()
