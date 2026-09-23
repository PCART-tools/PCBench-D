    def get_rows_with_mask(self, indexer: npt.NDArray[np.bool_]) -> Self:
        # similar to get_slice, but not restricted to slice indexer
        blk = self._block
        if using_copy_on_write() and len(indexer) > 0 and indexer.all():
            return type(self)(blk.copy(deep=False), self.index)
        array = blk.values[indexer]

        bp = BlockPlacement(slice(0, len(array)))
        # TODO(CoW) in theory only need to track reference if new_array is a view
        block = type(blk)(array, placement=bp, ndim=1, refs=blk.refs)

        new_idx = self.index[indexer]
        return type(self)(block, new_idx)
