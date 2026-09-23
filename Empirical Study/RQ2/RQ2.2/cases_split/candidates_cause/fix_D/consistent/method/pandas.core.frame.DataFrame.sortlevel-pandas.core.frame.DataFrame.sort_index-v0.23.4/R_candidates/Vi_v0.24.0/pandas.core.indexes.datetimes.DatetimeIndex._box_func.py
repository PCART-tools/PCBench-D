    @property
    def _box_func(self):
        return lambda x: Timestamp(x, tz=self.tz)
