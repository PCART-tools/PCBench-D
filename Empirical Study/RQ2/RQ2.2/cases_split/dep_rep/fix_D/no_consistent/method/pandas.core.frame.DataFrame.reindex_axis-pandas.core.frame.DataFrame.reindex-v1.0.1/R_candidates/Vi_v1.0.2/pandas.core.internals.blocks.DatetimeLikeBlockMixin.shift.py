    def shift(self, periods, axis=0, fill_value=None):
        # TODO(EA2D) this is unnecessary if these blocks are backed by 2D EAs
        values = self.array_values()
        new_values = values.shift(periods, fill_value=fill_value, axis=axis)
        return self.make_block_same_class(new_values)
