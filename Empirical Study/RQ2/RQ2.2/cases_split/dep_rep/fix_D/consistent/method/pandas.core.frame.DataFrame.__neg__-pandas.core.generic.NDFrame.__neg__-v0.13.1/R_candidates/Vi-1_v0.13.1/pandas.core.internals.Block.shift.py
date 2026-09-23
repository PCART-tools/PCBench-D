    def shift(self, indexer, periods, axis=0):
        """ shift the block by periods, possibly upcast """

        new_values = self.values.take(indexer, axis=axis)
        # convert integer to float if necessary. need to do a lot more than
        # that, handle boolean etc also
        new_values, fill_value = com._maybe_upcast(new_values)

        # 1-d
        if self.ndim == 1:
            if periods > 0:
                new_values[:periods] = fill_value
            else:
                new_values[periods:] = fill_value

        # 2-d
        else:
            if periods > 0:
                new_values[:, :periods] = fill_value
            else:
                new_values[:, periods:] = fill_value
        return [make_block(new_values, self.items, self.ref_items,
                           ndim=self.ndim, fastpath=True)]
