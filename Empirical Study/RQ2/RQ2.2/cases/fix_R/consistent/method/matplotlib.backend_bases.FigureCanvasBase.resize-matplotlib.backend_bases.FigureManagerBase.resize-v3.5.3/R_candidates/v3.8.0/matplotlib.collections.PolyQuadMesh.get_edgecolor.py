    def get_edgecolor(self):
        # docstring inherited
        # We only want to return the facecolors of the polygons
        # that were drawn.
        ec = super().get_edgecolor()
        unmasked_polys = self._get_unmasked_polys().ravel()
        if len(ec) != len(unmasked_polys):
            # Mapping is off
            return ec
        return ec[unmasked_polys, :]
