    def _interleave(self):
        """
        Return ndarray from blocks with specified item order
        Items must be contained in the blocks
        """
        dtype = _interleaved_dtype(self.blocks)

        result = np.empty(self.shape, dtype=dtype)

        if result.shape[0] == 0:
            # Workaround for numpy 1.7 bug:
            #
            #     >>> a = np.empty((0,10))
            #     >>> a[slice(0,0)]
            #     array([], shape=(0, 10), dtype=float64)
            #     >>> a[[]]
            #     Traceback (most recent call last):
            #       File "<stdin>", line 1, in <module>
            #     IndexError: index 0 is out of bounds for axis 0 with size 0
            return result

        itemmask = np.zeros(self.shape[0])

        for blk in self.blocks:
            rl = blk.mgr_locs
            result[rl.indexer] = blk.get_values(dtype)
            itemmask[rl.indexer] = 1

        if not itemmask.all():
            raise AssertionError('Some items were not contained in blocks')

        return result
