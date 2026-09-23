    def getitem_mgr(self, indexer: slice | npt.NDArray[np.bool_]) -> SingleBlockManager:
        # similar to get_slice, but not restricted to slice indexer
        blk = self._block
        array = blk._slice(indexer)
        if array.ndim > 1:
            # This will be caught by Series._get_values
            raise ValueError("dimension-expanding indexing not allowed")

        bp = BlockPlacement(slice(0, len(array)))
        block = type(blk)(array, placement=bp, ndim=1)

        new_idx = self.index[indexer]
        # TODO(CoW) in theory only need to track reference if new_array is a view
        ref = weakref.ref(blk)
        return type(self)(block, new_idx, [ref])
