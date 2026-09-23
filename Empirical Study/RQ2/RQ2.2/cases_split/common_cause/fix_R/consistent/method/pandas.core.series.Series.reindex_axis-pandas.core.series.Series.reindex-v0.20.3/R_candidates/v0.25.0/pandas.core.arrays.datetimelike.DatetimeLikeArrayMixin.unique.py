    def unique(self):
        result = unique1d(self.asi8)
        return type(self)(result, dtype=self.dtype)
