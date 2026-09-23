    def _interleave(self):
        """
        Return ndarray from blocks with specified item order
        Items must be contained in the blocks
        """
        from pandas.core.dtypes.common import is_sparse
        dtype = _interleaved_dtype(self.blocks)

        # TODO: https://github.com/pandas-dev/pandas/issues/22791
        # Give EAs some input on what happens here. Sparse needs this.
        if is_sparse(dtype):
            dtype = dtype.subtype
        elif is_extension_array_dtype(dtype):
            dtype = 'object'

        result = np.empty(self.shape, dtype=dtype)

        itemmask = np.zeros(self.shape[0])

        for blk in self.blocks:
            rl = blk.mgr_locs
            result[rl.indexer] = blk.get_values(dtype)
            itemmask[rl.indexer] = 1

        if not itemmask.all():
            raise AssertionError('Some items were not contained in blocks')

        return result
