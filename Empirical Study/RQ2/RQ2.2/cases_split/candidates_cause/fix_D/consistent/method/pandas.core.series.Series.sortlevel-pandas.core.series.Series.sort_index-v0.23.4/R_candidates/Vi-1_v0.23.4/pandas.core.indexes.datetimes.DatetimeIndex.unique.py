    def unique(self, level=None):
        # Override here since IndexOpsMixin.unique uses self._values.unique
        # For DatetimeIndex with TZ, that's a DatetimeIndex -> recursion error
        # So we extract the tz-naive DatetimeIndex, unique that, and wrap the
        # result with out TZ.
        if self.tz is not None:
            naive = type(self)(self._ndarray_values, copy=False)
        else:
            naive = self
        result = super(DatetimeIndex, naive).unique(level=level)
        return self._simple_new(result, name=self.name, tz=self.tz,
                                freq=self.freq)
