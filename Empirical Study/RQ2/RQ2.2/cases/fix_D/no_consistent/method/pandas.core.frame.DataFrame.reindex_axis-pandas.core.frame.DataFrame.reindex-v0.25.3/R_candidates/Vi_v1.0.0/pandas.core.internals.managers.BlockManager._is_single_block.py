    @property
    def _is_single_block(self):
        if self.ndim == 1:
            return True

        if len(self.blocks) != 1:
            return False

        blk = self.blocks[0]
        return blk.mgr_locs.is_slice_like and blk.mgr_locs.as_slice == slice(
            0, len(self), 1
        )
