    def set_capstyle(self, cs):
        """
        Set the capstyle for the collection (for all its elements).

        Parameters
        ----------
        cs : {'butt', 'round', 'projecting'}
            The capstyle
        """
        cbook._check_in_list(('butt', 'round', 'projecting'), capstyle=cs)
        self._capstyle = cs
