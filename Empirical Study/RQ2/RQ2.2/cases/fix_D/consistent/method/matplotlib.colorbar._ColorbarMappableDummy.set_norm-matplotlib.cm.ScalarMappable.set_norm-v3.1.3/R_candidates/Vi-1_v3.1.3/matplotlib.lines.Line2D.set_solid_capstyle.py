    def set_solid_capstyle(self, s):
        """
        Set the cap style for solid lines.

        Parameters
        ----------
        s : {'butt', 'round', 'projecting'}
        """
        s = s.lower()
        cbook._check_in_list(self.validCap, s=s)
        if self._solidcapstyle != s:
            self.stale = True
        self._solidcapstyle = s
