    def is_dashed(self):
        """
        Return whether line has a dashed linestyle.

        See also `~.Line2D.set_linestyle`.
        """
        return self._linestyle in ('--', '-.', ':')
