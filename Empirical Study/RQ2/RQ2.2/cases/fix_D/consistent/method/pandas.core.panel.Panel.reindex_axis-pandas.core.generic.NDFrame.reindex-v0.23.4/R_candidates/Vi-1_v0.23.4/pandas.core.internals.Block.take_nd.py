    def take_nd(self, indexer, axis, new_mgr_locs=None, fill_tuple=None):
        """
        Take values according to indexer and return them as a block.bb

        """

        # algos.take_nd dispatches for DatetimeTZBlock, CategoricalBlock
        # so need to preserve types
        # sparse is treated like an ndarray, but needs .get_values() shaping

        values = self.values
        if self.is_sparse:
            values = self.get_values()

        if fill_tuple is None:
            fill_value = self.fill_value
            new_values = algos.take_nd(values, indexer, axis=axis,
                                       allow_fill=False)
        else:
            fill_value = fill_tuple[0]
            new_values = algos.take_nd(values, indexer, axis=axis,
                                       allow_fill=True, fill_value=fill_value)

        if new_mgr_locs is None:
            if axis == 0:
                slc = libinternals.indexer_as_slice(indexer)
                if slc is not None:
                    new_mgr_locs = self.mgr_locs[slc]
                else:
                    new_mgr_locs = self.mgr_locs[indexer]
            else:
                new_mgr_locs = self.mgr_locs

        if not is_dtype_equal(new_values.dtype, self.dtype):
            return self.make_block(new_values, new_mgr_locs)
        else:
            return self.make_block_same_class(new_values, new_mgr_locs)
