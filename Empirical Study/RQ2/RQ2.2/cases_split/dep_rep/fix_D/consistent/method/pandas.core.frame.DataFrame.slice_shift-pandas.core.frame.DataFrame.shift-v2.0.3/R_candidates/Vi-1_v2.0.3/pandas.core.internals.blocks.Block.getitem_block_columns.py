    @final
    def getitem_block_columns(
        self, slicer: slice, new_mgr_locs: BlockPlacement
    ) -> Block:
        """
        Perform __getitem__-like, return result as block.

        Only supports slices that preserve dimensionality.
        """
        new_values = self._slice(slicer)

        if new_values.ndim != self.values.ndim:
            raise ValueError("Only same dim slicing is allowed")

        return type(self)(new_values, new_mgr_locs, self.ndim, refs=self.refs)
