    @property
    def _box_func(self):
        return lambda x: Timestamp(x, freq=self.offset, tz=self.tz)
