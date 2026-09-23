    def _set_x_filled(self):
        self._transform = Affine2D().translate(-0.5, -0.5)
        self._snap_threshold = 5.0
        self._joinstyle = 'miter'
        fs = self.get_fillstyle()
        if not self._half_fill():
            self._path = self._x_filled_path
        else:
            # Rotate top half path to support all partitions
            if fs == 'top':
                rotate, rotate_alt = 0, 180
            elif fs == 'bottom':
                rotate, rotate_alt = 180, 0
            elif fs == 'left':
                rotate, rotate_alt = 90, 270
            else:
                rotate, rotate_alt = 270, 90

            self._path = self._x_filled_path_t
            self._alt_path = self._x_filled_path_t
            self._alt_transform = Affine2D().translate(-0.5, -0.5)
            self._transform.rotate_deg(rotate)
            self._alt_transform.rotate_deg(rotate_alt)
