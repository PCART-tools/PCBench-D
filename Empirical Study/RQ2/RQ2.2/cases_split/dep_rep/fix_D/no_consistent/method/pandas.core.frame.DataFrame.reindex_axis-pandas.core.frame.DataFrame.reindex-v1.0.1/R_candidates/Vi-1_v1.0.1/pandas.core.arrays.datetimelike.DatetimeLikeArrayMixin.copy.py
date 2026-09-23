    def copy(self):
        values = self.asi8.copy()
        return type(self)._simple_new(values, dtype=self.dtype, freq=self.freq)
