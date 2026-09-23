    @property
    def _values(self):
        # tz-naive -> ndarray
        # tz-aware -> DatetimeIndex
        if self.tz is not None:
            return self
        else:
            return self.values
