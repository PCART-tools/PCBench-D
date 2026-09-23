    def __init__(
        self,
        blocks: Sequence[Block],
        axes: Sequence[Index],
        do_integrity_check: bool = True,
    ):
        self.axes = [ensure_index(ax) for ax in axes]
        self.blocks: Tuple[Block, ...] = tuple(blocks)

        for block in blocks:
            if self.ndim != block.ndim:
                raise AssertionError(
                    f"Number of Block dimensions ({block.ndim}) must equal "
                    f"number of axes ({self.ndim})"
                )

        if do_integrity_check:
            self._verify_integrity()

        self._consolidate_check()

        self._rebuild_blknos_and_blklocs()
