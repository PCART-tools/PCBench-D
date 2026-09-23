    def __init__(
        self,
        blocks: Sequence[Block],
        axes: Sequence[Index],
        do_integrity_check: bool = True,
    ):
        self.axes = [ensure_index(ax) for ax in axes]
        self.blocks = tuple(blocks)  # type: Tuple[Block, ...]

        for block in blocks:
            if self.ndim != block.ndim:
                raise AssertionError(
                    "Number of Block dimensions ({block}) must equal "
                    "number of axes ({self})".format(block=block.ndim, self=self.ndim)
                )

        if do_integrity_check:
            self._verify_integrity()

        self._consolidate_check()

        self._rebuild_blknos_and_blklocs()
