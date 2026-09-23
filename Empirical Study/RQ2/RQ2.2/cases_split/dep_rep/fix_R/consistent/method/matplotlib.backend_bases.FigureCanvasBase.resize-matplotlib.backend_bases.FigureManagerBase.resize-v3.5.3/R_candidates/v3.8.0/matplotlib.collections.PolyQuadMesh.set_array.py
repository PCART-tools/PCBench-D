    def set_array(self, A):
        # docstring inherited
        prev_unmask = self._get_unmasked_polys()
        # MPL <3.8 compressed the mask, so we need to handle flattened 1d input
        # until the deprecation expires, also only warning when there are masked
        # elements and thus compression occurring.
        if self._deprecated_compression and np.ndim(A) == 1:
            _api.warn_deprecated("3.8", message="Setting a PolyQuadMesh array using "
                                 "the compressed values is deprecated. "
                                 "Pass the full 2D shape of the original array "
                                 f"{prev_unmask.shape} including the masked elements.")
            Afull = np.empty(self._original_mask.shape)
            Afull[~self._original_mask] = A
            # We also want to update the mask with any potential
            # new masked elements that came in. But, we don't want
            # to update any of the compression from the original
            mask = self._original_mask.copy()
            mask[~self._original_mask] |= np.ma.getmask(A)
            A = np.ma.array(Afull, mask=mask)
            return super().set_array(A)
        self._deprecated_compression = False
        super().set_array(A)
        # If the mask has changed at all we need to update
        # the set of Polys that we are drawing
        if not np.array_equal(prev_unmask, self._get_unmasked_polys()):
            self._set_unmasked_verts()
