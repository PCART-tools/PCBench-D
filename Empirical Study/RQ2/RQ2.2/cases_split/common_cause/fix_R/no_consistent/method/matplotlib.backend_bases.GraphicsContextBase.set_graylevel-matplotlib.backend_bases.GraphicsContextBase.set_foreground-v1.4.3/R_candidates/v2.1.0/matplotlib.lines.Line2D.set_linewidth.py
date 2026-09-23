    def set_linewidth(self, w):
        """
        Set the line width in points

        ACCEPTS: float value in points
        """
        w = float(w)

        if self._linewidth != w:
            self.stale = True
        self._linewidth = w
        # rescale the dashes + offset
        self._dashOffset, self._dashSeq = _scale_dashes(
            self._us_dashOffset, self._us_dashSeq, self._linewidth)
