    @property
    def _box_func(self):
        return lambda x: tslib.Timestamp(x, tz=self.dtype.tz)
