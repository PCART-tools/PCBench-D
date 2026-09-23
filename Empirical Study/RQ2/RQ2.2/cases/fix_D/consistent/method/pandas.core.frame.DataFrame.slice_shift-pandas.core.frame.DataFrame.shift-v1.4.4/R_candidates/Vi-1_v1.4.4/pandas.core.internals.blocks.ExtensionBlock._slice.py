    def _slice(self, slicer) -> ExtensionArray:
        """
        Return a slice of my values.

        Parameters
        ----------
        slicer : slice, ndarray[int], or a tuple of these
            Valid (non-reducing) indexer for self.values.

        Returns
        -------
        ExtensionArray
        """
        # return same dims as we currently have
        if not isinstance(slicer, tuple) and self.ndim == 2:
            # reached via getitem_block via _slice_take_blocks_ax0
            # TODO(EA2D): won't be necessary with 2D EAs
            slicer = (slicer, slice(None))

        if isinstance(slicer, tuple) and len(slicer) == 2:
            first = slicer[0]
            if not isinstance(first, slice):
                raise AssertionError(
                    "invalid slicing for a 1-ndim ExtensionArray", first
                )
            # GH#32959 only full-slicers along fake-dim0 are valid
            # TODO(EA2D): won't be necessary with 2D EAs
            # range(1) instead of self._mgr_locs to avoid exception on [::-1]
            #  see test_iloc_getitem_slice_negative_step_ea_block
            new_locs = range(1)[first]
            if len(new_locs):
                # effectively slice(None)
                slicer = slicer[1]
            else:
                raise AssertionError(
                    "invalid slicing for a 1-ndim ExtensionArray", slicer
                )

        return self.values[slicer]
