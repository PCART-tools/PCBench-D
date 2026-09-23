    def shift(self, indexer, periods, axis=0):
        """ shift the block by periods """

        new_values = self.values.to_dense().take(indexer)
        # convert integer to float if necessary. need to do a lot more than
        # that, handle boolean etc also
        new_values, fill_value = com._maybe_upcast(new_values)
        if periods > 0:
            new_values[:periods] = fill_value
        else:
            new_values[periods:] = fill_value
        return [self.make_block(new_values)]
