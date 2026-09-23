    def getitem_mgr(self, indexer) -> SingleBlockManager:
        # similar to get_slice, but not restricted to slice indexer
        blk = self._block
        array = blk._slice(indexer)
        if array.ndim > 1:
            # This will be caught by Series._get_values
            raise ValueError("dimension-expanding indexing not allowed")

        bp = BlockPlacement(slice(0, len(array)))
        block = type(blk)(array, placement=bp, ndim=1)

        new_idx = self.index[indexer]
        return type(self)(block, new_idx)
