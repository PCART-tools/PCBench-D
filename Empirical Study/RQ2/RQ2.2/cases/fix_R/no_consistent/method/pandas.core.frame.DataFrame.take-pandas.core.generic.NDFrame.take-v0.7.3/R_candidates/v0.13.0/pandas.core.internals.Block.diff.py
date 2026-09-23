    def diff(self, n):
        """ return block for the diff of the values """
        new_values = com.diff(self.values, n, axis=1)
        return [make_block(new_values, self.items, self.ref_items,
                           ndim=self.ndim, fastpath=True)]
