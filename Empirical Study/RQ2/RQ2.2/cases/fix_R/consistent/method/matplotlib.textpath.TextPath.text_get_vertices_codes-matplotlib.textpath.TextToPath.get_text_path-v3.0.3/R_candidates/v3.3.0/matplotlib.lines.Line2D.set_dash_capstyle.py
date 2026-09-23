    def set_dash_capstyle(self, s):
        """
        Set the cap style for dashed lines.

        Parameters
        ----------
        s : {'butt', 'round', 'projecting'}
            For examples see :doc:`/gallery/lines_bars_and_markers/joinstyle`.
        """
        mpl.rcsetup.validate_capstyle(s)
        if self._dashcapstyle != s:
            self.stale = True
        self._dashcapstyle = s
