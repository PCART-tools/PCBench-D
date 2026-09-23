    def _set_square(self):
        self._transform = Affine2D().translate(-0.5, -0.5)
        self._snap_threshold = 2.0
        fs = self.get_fillstyle()
        if not self._half_fill():
            self._path = Path.unit_rectangle()
        else:
            # build a bottom filled square out of two rectangles, one
            # filled.  Use the rotation to support left, right, bottom
            # or top
            if fs == 'bottom':
                rotate = 0.
            elif fs == 'top':
                rotate = 180.
            elif fs == 'left':
                rotate = 270.
            else:
                rotate = 90.

            self._path = Path([[0.0, 0.0], [1.0, 0.0], [1.0, 0.5],
                               [0.0, 0.5], [0.0, 0.0]])
            self._alt_path = Path([[0.0, 0.5], [1.0, 0.5], [1.0, 1.0],
                                   [0.0, 1.0], [0.0, 0.5]])
            self._transform.rotate_deg(rotate)
            self._alt_transform = self._transform

        self._joinstyle = 'miter'
