    def to_2d_mgr(self, columns: Index) -> BlockManager:
        """
        Manager analogue of Series.to_frame
        """
        blk = self.blocks[0]
        arr = ensure_block_shape(blk.values, ndim=2)
        bp = BlockPlacement(0)
        new_blk = type(blk)(arr, placement=bp, ndim=2)
        axes = [columns, self.axes[0]]
        refs: list[weakref.ref | None] = [weakref.ref(blk)]
        return BlockManager([new_blk], axes=axes, refs=refs, verify_integrity=False)
