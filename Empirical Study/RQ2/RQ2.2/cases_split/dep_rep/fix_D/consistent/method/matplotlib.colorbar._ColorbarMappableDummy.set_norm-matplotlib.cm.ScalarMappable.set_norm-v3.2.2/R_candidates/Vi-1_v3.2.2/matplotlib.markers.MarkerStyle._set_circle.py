    def _set_circle(self, reduction=1.0):
        self._transform = Affine2D().scale(0.5 * reduction)
        self._snap_threshold = np.inf
        fs = self.get_fillstyle()
        if not self._half_fill():
            self._path = Path.unit_circle()
        else:
            # build a right-half circle
            if fs == 'bottom':
                rotate = 270.
            elif fs == 'top':
                rotate = 90.
            elif fs == 'left':
                rotate = 180.
            else:
                rotate = 0.

            self._path = self._alt_path = Path.unit_circle_righthalf()
            self._transform.rotate_deg(rotate)
            self._alt_transform = self._transform.frozen().rotate_deg(180.)
