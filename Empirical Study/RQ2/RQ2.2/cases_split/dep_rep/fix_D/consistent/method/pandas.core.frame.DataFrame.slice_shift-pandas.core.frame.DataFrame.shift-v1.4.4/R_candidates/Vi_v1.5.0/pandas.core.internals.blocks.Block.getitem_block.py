    @final
    def getitem_block(self, slicer: slice | npt.NDArray[np.intp]) -> Block:
        """
        Perform __getitem__-like, return result as block.

        Only supports slices that preserve dimensionality.
        """
        # Note: the only place where we are called with ndarray[intp]
        #  is from internals.concat, and we can verify that never happens
        #  with 1-column blocks, i.e. never for ExtensionBlock.

        # Invalid index type "Union[slice, ndarray[Any, dtype[signedinteger[Any]]]]"
        # for "BlockPlacement"; expected type "Union[slice, Sequence[int]]"
        new_mgr_locs = self._mgr_locs[slicer]  # type: ignore[index]

        new_values = self._slice(slicer)

        if new_values.ndim != self.values.ndim:
            raise ValueError("Only same dim slicing is allowed")

        return type(self)(new_values, new_mgr_locs, self.ndim)
