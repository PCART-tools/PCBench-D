    def set_array(self, A):
        # docstring inherited
        prev_unmask = self._get_unmasked_polys()
        super().set_array(A)
        # If the mask has changed at all we need to update
        # the set of Polys that we are drawing
        if not np.array_equal(prev_unmask, self._get_unmasked_polys()):
            self._set_unmasked_verts()
