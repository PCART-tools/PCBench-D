    def set_capstyle(self, s):
        """
        Set the capstyle.

        Parameters
        ----------
        s : {'butt', 'round', 'projecting'}
        """
        s = s.lower()
        cbook._check_in_list(self.validCap, capstyle=s)
        self._capstyle = s
        self.stale = True
