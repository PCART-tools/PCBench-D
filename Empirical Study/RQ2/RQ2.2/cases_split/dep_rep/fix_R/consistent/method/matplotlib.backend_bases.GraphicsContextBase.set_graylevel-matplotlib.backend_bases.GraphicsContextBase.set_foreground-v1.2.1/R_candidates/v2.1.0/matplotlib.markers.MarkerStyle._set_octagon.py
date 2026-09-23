    def _set_octagon(self):
        self._transform = Affine2D().scale(0.5)
        self._snap_threshold = 5.0

        fs = self.get_fillstyle()
        polypath = Path.unit_regular_polygon(8)

        if not self._half_fill():
            self._transform.rotate_deg(22.5)
            self._path = polypath
        else:
            x = np.sqrt(2.) / 4.
            half = Path([[0, -1], [0, 1], [-x, 1], [-1, x],
                         [-1, -x], [-x, -1], [0, -1]])

            if fs == 'bottom':
                rotate = 90.
            elif fs == 'top':
                rotate = 270.
            elif fs == 'right':
                rotate = 180.
            else:
                rotate = 0.

            self._transform.rotate_deg(rotate)
            self._path = self._alt_path = half
            self._alt_transform = self._transform.frozen().rotate_deg(180.0)

        self._joinstyle = 'miter'
