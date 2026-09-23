    @classmethod
    def from_array(
        cls, array: ArrayLike, index: Index, refs: BlockValuesRefs | None = None
    ) -> SingleBlockManager:
        """
        Constructor for if we have an array that is not yet a Block.
        """
        array = maybe_coerce_values(array)
        bp = BlockPlacement(slice(0, len(index)))
        block = new_block(array, placement=bp, ndim=1, refs=refs)
        return cls(block, index)
