    def _set_diamond(self):
        self._transform = Affine2D().translate(-0.5, -0.5).rotate_deg(45)
        self._snap_threshold = 5.0
        fs = self.get_fillstyle()
        if not self._half_fill():
            self._path = Path.unit_rectangle()
        else:
            self._path = Path([[0, 0], [1, 0], [1, 1], [0, 0]])
            self._alt_path = Path([[0, 0], [0, 1], [1, 1], [0, 0]])
            if fs == 'bottom':
                rotate = 270.
            elif fs == 'top':
                rotate = 90.
            elif fs == 'left':
                rotate = 180.
            else:
                rotate = 0.
            self._transform.rotate_deg(rotate)
            self._alt_transform = self._transform
        self._joinstyle = 'miter'
