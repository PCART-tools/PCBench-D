    def set_values(self, values: ArrayLike):
        """
        Set the values of the single block in place.

        Use at your own risk! This does not check if the passed values are
        valid for the current Block/SingleBlockManager (length, dtype, etc).
        """
        # TODO(CoW) do we need to handle copy on write here? Currently this is
        # only used for FrameColumnApply.series_generator (what if apply is
        # mutating inplace?)
        self.blocks[0].values = values
        self.blocks[0]._mgr_locs = BlockPlacement(slice(len(values)))
