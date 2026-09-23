    def _set_circle(self, reduction=1.0):
        self._transform = Affine2D().scale(0.5 * reduction)
        self._snap_threshold = np.inf
        if not self._half_fill():
            self._path = Path.unit_circle()
        else:
            self._path = self._alt_path = Path.unit_circle_righthalf()
            fs = self.get_fillstyle()
            self._transform.rotate_deg(
                {'right': 0, 'top': 90, 'left': 180, 'bottom': 270}[fs])
            self._alt_transform = self._transform.frozen().rotate_deg(180.)
