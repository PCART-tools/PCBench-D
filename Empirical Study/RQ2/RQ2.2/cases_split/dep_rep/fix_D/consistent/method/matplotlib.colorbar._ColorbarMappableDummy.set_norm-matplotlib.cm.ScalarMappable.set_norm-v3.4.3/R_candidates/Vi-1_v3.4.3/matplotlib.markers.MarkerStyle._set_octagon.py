    def _set_octagon(self):
        self._transform = Affine2D().scale(0.5)
        self._snap_threshold = 5.0

        polypath = Path.unit_regular_polygon(8)

        if not self._half_fill():
            self._transform.rotate_deg(22.5)
            self._path = polypath
        else:
            x = np.sqrt(2.) / 4.
            self._path = self._alt_path = Path(
                [[0, -1], [0, 1], [-x, 1], [-1, x],
                 [-1, -x], [-x, -1], [0, -1]])
            fs = self.get_fillstyle()
            self._transform.rotate_deg(
                {'left': 0, 'bottom': 90, 'right': 180, 'top': 270}[fs])
            self._alt_transform = self._transform.frozen().rotate_deg(180.0)

        self._joinstyle = JoinStyle.miter
