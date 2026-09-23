    @classmethod
    def from_blocks(
        cls,
        blocks: list[Block],
        axes: list[Index],
        refs: list[weakref.ref | None] | None = None,
    ) -> BlockManager:
        """
        Constructor for BlockManager and SingleBlockManager with same signature.
        """
        return cls(blocks, axes, refs, verify_integrity=False)
