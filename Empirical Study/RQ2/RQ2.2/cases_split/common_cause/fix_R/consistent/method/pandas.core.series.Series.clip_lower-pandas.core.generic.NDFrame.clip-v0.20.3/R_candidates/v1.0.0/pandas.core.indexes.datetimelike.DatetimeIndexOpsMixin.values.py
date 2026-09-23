    @property
    def values(self):
        # Note: PeriodArray overrides this to return an ndarray of objects.
        return self._data._data
