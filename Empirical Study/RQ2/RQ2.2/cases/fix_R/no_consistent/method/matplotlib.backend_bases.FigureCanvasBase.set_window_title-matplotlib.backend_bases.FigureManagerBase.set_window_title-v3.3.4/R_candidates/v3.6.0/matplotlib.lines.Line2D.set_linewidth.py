    def set_linewidth(self, w):
        """
        Set the line width in points.

        Parameters
        ----------
        w : float
            Line width, in points.
        """
        w = float(w)
        if self._linewidth != w:
            self.stale = True
        self._linewidth = w
        self._dash_pattern = _scale_dashes(*self._unscaled_dash_pattern, w)
