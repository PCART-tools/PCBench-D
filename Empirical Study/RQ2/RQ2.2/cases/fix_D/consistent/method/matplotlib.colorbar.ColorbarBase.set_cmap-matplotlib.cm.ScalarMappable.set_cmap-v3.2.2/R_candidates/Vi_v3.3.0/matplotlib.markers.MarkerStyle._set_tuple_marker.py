    def _set_tuple_marker(self):
        marker = self._marker
        if len(marker) == 2:
            numsides, rotation = marker[0], 0.0
        elif len(marker) == 3:
            numsides, rotation = marker[0], marker[2]
        symstyle = marker[1]
        if symstyle == 0:
            self._path = Path.unit_regular_polygon(numsides)
            self._joinstyle = 'miter'
        elif symstyle == 1:
            self._path = Path.unit_regular_star(numsides)
            self._joinstyle = 'bevel'
        elif symstyle == 2:
            self._path = Path.unit_regular_asterisk(numsides)
            self._filled = False
            self._joinstyle = 'bevel'
        else:
            raise ValueError(f"Unexpected tuple marker: {marker}")
        self._transform = Affine2D().scale(0.5).rotate_deg(rotation)
