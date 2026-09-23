    def get_facecolor(self):
        # docstring inherited
        # We only want to return the facecolors of the polygons
        # that were drawn.
        fc = super().get_facecolor()
        unmasked_polys = self._get_unmasked_polys().ravel()
        if len(fc) != len(unmasked_polys):
            # Mapping is off
            return fc
        return fc[unmasked_polys, :]
