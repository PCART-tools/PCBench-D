    @fill_value.setter
    def fill_value(self, v):
        # we may need to upcast our fill to match our dtype
        if issubclass(self.dtype.type, np.floating):
            v = float(v)
        self.values.fill_value = v
