    def set_joinstyle(self, s):
        """Set the joinstyle.

        Parameters
        ----------
        s : {'miter', 'round', 'bevel'}
        """
        s = s.lower()
        cbook._check_in_list(self.validJoin, joinstyle=s)
        self._joinstyle = s
        self.stale = True
