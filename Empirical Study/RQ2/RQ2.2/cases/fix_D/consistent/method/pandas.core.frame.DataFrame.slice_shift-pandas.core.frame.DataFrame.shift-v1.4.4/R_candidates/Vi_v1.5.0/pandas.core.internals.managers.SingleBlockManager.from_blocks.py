    @classmethod
    def from_blocks(
        cls,
        blocks: list[Block],
        axes: list[Index],
        refs: list[weakref.ref | None] | None = None,
    ) -> SingleBlockManager:
        """
        Constructor for BlockManager and SingleBlockManager with same signature.
        """
        assert len(blocks) == 1
        assert len(axes) == 1
        if refs is not None:
            assert len(refs) == 1
        return cls(blocks[0], axes[0], refs, verify_integrity=False)
