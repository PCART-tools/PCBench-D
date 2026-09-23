    @property
    def _box_func(self):
        return lambda x: tslibs.Timestamp(x, tz=self.dtype.tz)
