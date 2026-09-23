    def _recache(self):
        if self._marker_function is None:
            return
        self._path = _empty_path
        self._transform = IdentityTransform()
        self._alt_path = None
        self._alt_transform = None
        self._snap_threshold = None
        self._joinstyle = JoinStyle.round
        self._capstyle = CapStyle.butt
        # Initial guess: Assume the marker is filled unless the fillstyle is
        # set to 'none'. The marker function will override this for unfilled
        # markers.
        self._filled = self._fillstyle != 'none'
        self._marker_function()
