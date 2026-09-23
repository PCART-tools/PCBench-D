    def contains(self, mouseevent):
        """Test whether the artist contains the mouse event.

        Returns the truth value and a dictionary of artist specific details of
        selection, such as which points are contained in the pick radius.  See
        individual artists for details.
        """
        if callable(self._contains):
            return self._contains(self, mouseevent)
        warnings.warn("'%s' needs 'contains' method" % self.__class__.__name__)
        return False, {}
