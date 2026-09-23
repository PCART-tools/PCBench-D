    @classmethod
    def from_array(
        cls, array: ArrayLike, index: Index, refs: BlockValuesRefs | None = None
    ) -> SingleBlockManager:
        """
        Constructor for if we have an array that is not yet a Block.
        """
        block = new_block(array, placement=slice(0, len(index)), ndim=1, refs=refs)
        return cls(block, index)
