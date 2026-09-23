    def set_capstyle(self, cs):
        """
        Set the capstyle for the collection. The capstyle can
        only be set globally for all elements in the collection

        Parameters
        ----------
        cs : {'butt', 'round', 'projecting'}
            The capstyle
        """
        if cs in ('butt', 'round', 'projecting'):
            self._capstyle = cs
        else:
            raise ValueError('Unrecognized cap style.  Found %s' % cs)
