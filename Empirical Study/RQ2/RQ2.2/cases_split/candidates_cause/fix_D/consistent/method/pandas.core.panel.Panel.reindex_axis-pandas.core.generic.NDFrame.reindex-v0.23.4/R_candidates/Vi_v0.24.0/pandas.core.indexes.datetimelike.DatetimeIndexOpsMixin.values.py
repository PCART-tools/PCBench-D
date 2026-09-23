    @property
    def values(self):
        # type: () -> np.ndarray
        # Note: PeriodArray overrides this to return an ndarray of objects.
        return self._data._data
