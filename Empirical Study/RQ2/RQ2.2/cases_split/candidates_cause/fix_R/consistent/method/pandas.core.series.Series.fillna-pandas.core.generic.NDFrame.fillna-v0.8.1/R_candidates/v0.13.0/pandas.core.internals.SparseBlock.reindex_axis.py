    def reindex_axis(self, indexer, method=None, axis=1, fill_value=None,
                     limit=None, mask_info=None):
        """
        Reindex using pre-computed indexer information
        """
        if axis < 1:
            raise AssertionError('axis must be at least 1, got %d' % axis)

        # taking on the 0th axis always here
        if fill_value is None:
            fill_value = self.fill_value
        return self.make_block(self.values.take(indexer), items=self.items,
                               fill_value=fill_value)
