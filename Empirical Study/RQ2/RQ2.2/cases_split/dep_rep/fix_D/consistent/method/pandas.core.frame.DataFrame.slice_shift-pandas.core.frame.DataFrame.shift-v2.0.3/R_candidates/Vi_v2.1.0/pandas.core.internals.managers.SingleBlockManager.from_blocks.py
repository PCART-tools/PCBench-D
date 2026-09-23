    @classmethod
    def from_blocks(
        cls,
        blocks: list[Block],
        axes: list[Index],
    ) -> Self:
        """
        Constructor for BlockManager and SingleBlockManager with same signature.
        """
        assert len(blocks) == 1
        assert len(axes) == 1
        return cls(blocks[0], axes[0], verify_integrity=False)
