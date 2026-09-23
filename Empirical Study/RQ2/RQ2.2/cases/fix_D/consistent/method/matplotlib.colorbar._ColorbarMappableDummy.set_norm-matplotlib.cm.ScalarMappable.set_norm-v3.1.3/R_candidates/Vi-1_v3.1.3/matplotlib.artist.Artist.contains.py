    def contains(self, mouseevent):
        """Test whether the artist contains the mouse event.

        Parameters
        ----------
        mouseevent : `matplotlib.backend_bases.MouseEvent`

        Returns
        -------
        contains : bool
            Whether any values are within the radius.
        details : dict
            An artist-specific dictionary of details of the event context,
            such as which points are contained in the pick radius. See the
            individual Artist subclasses for details.

        See Also
        --------
        set_contains, get_contains
        """
        if self._contains is not None:
            return self._contains(self, mouseevent)
        _log.warning("%r needs 'contains' method", self.__class__.__name__)
        return False, {}
