    def set_solid_capstyle(self, s):
        """
        Set the cap style for solid lines.

        Parameters
        ----------
        s : {'butt', 'round', 'projecting'}
            For examples see :doc:`/gallery/lines_bars_and_markers/joinstyle`.
        """
        mpl.rcsetup.validate_capstyle(s)
        if self._solidcapstyle != s:
            self.stale = True
        self._solidcapstyle = s
