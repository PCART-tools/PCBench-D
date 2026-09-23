    def set_capstyle(self, s):
        """
        Set the capstyle.

        Parameters
        ----------
        s : {'butt', 'round', 'projecting'}
        """
        mpl.rcsetup.validate_capstyle(s)
        self._capstyle = s
        self.stale = True
