    def __init__(
        self,
        block: Block,
        axis: Index,
        verify_integrity: bool = False,
        fastpath=lib.no_default,
    ):
        # Assertions disabled for performance
        # assert isinstance(block, Block), type(block)
        # assert isinstance(axis, Index), type(axis)

        if fastpath is not lib.no_default:
            warnings.warn(
                "The `fastpath` keyword is deprecated and will be removed "
                "in a future version.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )

        self.axes = [axis]
        self.blocks = (block,)
