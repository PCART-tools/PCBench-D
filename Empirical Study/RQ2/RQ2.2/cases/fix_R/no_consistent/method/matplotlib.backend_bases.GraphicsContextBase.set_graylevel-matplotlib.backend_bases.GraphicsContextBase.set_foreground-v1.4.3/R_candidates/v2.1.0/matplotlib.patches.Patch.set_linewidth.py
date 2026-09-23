    def set_linewidth(self, w):
        """
        Set the patch linewidth in points

        ACCEPTS: float or None for default
        """
        if w is None:
            w = mpl.rcParams['patch.linewidth']
            if w is None:
                w = mpl.rcParams['axes.linewidth']

        self._linewidth = float(w)
        # scale the dash pattern by the linewidth
        offset, ls = self._us_dashes
        self._dashoffset, self._dashes = mlines._scale_dashes(
            offset, ls, self._linewidth)
        self.stale = True
