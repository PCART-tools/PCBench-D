    def set_joinstyle(self, s):
        """
        Set the joinstyle.

        Parameters
        ----------
        s : {'miter', 'round', 'bevel'}
        """
        mpl.rcsetup.validate_joinstyle(s)
        self._joinstyle = s
        self.stale = True
