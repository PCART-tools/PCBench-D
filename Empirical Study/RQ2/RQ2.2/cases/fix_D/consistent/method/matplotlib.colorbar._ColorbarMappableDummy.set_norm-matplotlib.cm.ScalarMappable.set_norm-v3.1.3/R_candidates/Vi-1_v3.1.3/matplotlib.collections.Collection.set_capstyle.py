    def set_capstyle(self, cs):
        """
        Set the capstyle for the collection (for all its elements).

        Parameters
        ----------
        cs : {'butt', 'round', 'projecting'}
            The capstyle
        """
        if cs in ('butt', 'round', 'projecting'):
            self._capstyle = cs
        else:
            raise ValueError('Unrecognized cap style.  Found %s' % cs)
