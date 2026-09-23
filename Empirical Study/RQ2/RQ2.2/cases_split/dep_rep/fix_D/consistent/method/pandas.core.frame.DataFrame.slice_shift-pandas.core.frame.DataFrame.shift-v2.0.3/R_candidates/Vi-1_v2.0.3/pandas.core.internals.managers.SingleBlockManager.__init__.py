    def __init__(
        self,
        block: Block,
        axis: Index,
        verify_integrity: bool = False,
    ) -> None:
        # Assertions disabled for performance
        # assert isinstance(block, Block), type(block)
        # assert isinstance(axis, Index), type(axis)

        self.axes = [axis]
        self.blocks = (block,)
