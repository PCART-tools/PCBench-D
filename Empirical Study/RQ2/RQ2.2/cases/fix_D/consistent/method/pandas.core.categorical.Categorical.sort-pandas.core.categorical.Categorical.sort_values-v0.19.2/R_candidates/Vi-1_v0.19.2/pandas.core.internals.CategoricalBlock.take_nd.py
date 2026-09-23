    def take_nd(self, indexer, axis=0, new_mgr_locs=None, fill_tuple=None):
        """
        Take values according to indexer and return them as a block.bb
        """
        if fill_tuple is None:
            fill_value = None
        else:
            fill_value = fill_tuple[0]

        # axis doesn't matter; we are really a single-dim object
        # but are passed the axis depending on the calling routing
        # if its REALLY axis 0, then this will be a reindex and not a take
        new_values = self.values.take_nd(indexer, fill_value=fill_value)

        # if we are a 1-dim object, then always place at 0
        if self.ndim == 1:
            new_mgr_locs = [0]
        else:
            if new_mgr_locs is None:
                new_mgr_locs = self.mgr_locs

        return self.make_block_same_class(new_values, new_mgr_locs)
