    def reindex_axis(self, indexer, method=None, axis=1, fill_value=None,
                     limit=None, mask_info=None):
        """
        Reindex using pre-computed indexer information
        """
        if axis < 1:
            raise AssertionError('axis must be at least 1, got %d' % axis)
        if fill_value is None:
            fill_value = self.fill_value

        new_values = com.take_nd(self.values, indexer, axis,
                                 fill_value=fill_value, mask_info=mask_info)
        return make_block(new_values,
                          ndim=self.ndim, fastpath=True,
                          placement=self.mgr_locs)
