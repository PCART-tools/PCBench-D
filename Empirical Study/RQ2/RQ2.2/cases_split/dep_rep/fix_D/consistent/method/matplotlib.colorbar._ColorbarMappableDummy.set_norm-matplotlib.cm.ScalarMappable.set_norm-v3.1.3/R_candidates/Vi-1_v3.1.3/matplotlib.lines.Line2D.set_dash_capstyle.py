    def set_dash_capstyle(self, s):
        """
        Set the cap style for dashed lines.

        Parameters
        ----------
        s : {'butt', 'round', 'projecting'}
        """
        s = s.lower()
        cbook._check_in_list(self.validCap, s=s)
        if self._dashcapstyle != s:
            self.stale = True
        self._dashcapstyle = s
