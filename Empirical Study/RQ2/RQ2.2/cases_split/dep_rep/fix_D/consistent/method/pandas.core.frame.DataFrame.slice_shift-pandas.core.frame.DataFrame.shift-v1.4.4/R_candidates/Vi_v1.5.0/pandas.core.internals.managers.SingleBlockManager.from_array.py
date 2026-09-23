    @classmethod
    def from_array(cls, array: ArrayLike, index: Index) -> SingleBlockManager:
        """
        Constructor for if we have an array that is not yet a Block.
        """
        block = new_block(array, placement=slice(0, len(index)), ndim=1)
        return cls(block, index)
