    def _set_square(self):
        self._transform = Affine2D().translate(-0.5, -0.5)
        self._snap_threshold = 2.0
        if not self._half_fill():
            self._path = Path.unit_rectangle()
        else:
            # Build a bottom filled square out of two rectangles, one filled.
            self._path = Path([[0.0, 0.0], [1.0, 0.0], [1.0, 0.5],
                               [0.0, 0.5], [0.0, 0.0]])
            self._alt_path = Path([[0.0, 0.5], [1.0, 0.5], [1.0, 1.0],
                                   [0.0, 1.0], [0.0, 0.5]])
            fs = self.get_fillstyle()
            rotate = {'bottom': 0, 'right': 90, 'top': 180, 'left': 270}[fs]
            self._transform.rotate_deg(rotate)
            self._alt_transform = self._transform

        self._joinstyle = JoinStyle.miter
