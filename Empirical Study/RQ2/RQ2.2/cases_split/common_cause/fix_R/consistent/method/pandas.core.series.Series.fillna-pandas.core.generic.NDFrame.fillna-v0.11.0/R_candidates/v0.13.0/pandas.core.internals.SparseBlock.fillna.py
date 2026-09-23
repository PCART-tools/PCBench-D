    def fillna(self, value, inplace=False, downcast=None):
        # we may need to upcast our fill to match our dtype
        if issubclass(self.dtype.type, np.floating):
            value = float(value)
        values = self.values if inplace else self.values.copy()
        return [self.make_block(values.get_values(value), fill_value=value)]
