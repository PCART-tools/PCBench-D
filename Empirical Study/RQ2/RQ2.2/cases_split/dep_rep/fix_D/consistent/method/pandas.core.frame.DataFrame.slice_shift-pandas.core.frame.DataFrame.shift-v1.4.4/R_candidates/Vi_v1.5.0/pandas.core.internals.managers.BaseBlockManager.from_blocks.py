    @classmethod
    def from_blocks(
        cls: type_t[T],
        blocks: list[Block],
        axes: list[Index],
        refs: list[weakref.ref | None] | None = None,
    ) -> T:
        raise NotImplementedError
