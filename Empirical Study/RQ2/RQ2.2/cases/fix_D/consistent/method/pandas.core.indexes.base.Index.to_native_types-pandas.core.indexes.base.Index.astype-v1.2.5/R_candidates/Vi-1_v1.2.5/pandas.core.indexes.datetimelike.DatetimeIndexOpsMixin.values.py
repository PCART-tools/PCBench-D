    @property
    def values(self) -> np.ndarray:
        # Note: PeriodArray overrides this to return an ndarray of objects.
        return self._data._data
