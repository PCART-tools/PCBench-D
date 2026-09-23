    def set_dash_capstyle(self, s):
        """
        Set the cap style for dashed linestyles.

        Parameters
        ----------
        s : {'butt', 'round', 'projecting'}
        """
        s = s.lower()
        if s not in self.validCap:
            raise ValueError('set_dash_capstyle passed "%s";\n' % (s,)
                             + 'valid capstyles are %s' % (self.validCap,))
        if self._dashcapstyle != s:
            self.stale = True
        self._dashcapstyle = s
