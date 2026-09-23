    def set_capstyle(self, cs):
        """
        Set the capstyle for the collection (for all its elements).

        Parameters
        ----------
        cs : {'butt', 'round', 'projecting'}
            The capstyle.
        """
        mpl.rcsetup.validate_capstyle(cs)
        self._capstyle = cs
