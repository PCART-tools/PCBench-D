    @classmethod
    def from_blocks(cls, blocks: list[Block], axes: list[Index]) -> Self:
        """
        Constructor for BlockManager and SingleBlockManager with same signature.
        """
        return cls(blocks, axes, verify_integrity=False)
