    @final
    def getitem_block(self, slicer: slice | npt.NDArray[np.intp]) -> Block:
        """
        Perform __getitem__-like, return result as block.

        Only supports slices that preserve dimensionality.
        """
        axis0_slicer = slicer[0] if isinstance(slicer, tuple) else slicer
        new_mgr_locs = self._mgr_locs[axis0_slicer]

        new_values = self._slice(slicer)

        if new_values.ndim != self.values.ndim:
            raise ValueError("Only same dim slicing is allowed")

        return type(self)(new_values, new_mgr_locs, self.ndim)
