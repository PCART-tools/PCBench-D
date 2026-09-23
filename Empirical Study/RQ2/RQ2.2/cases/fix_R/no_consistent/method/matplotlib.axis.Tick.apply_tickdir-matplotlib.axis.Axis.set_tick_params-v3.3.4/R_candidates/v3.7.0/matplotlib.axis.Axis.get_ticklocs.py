    def get_ticklocs(self, *, minor=False):
        """
        Return this Axis' tick locations in data coordinates.

        The locations are not clipped to the current axis limits and hence
        may contain locations that are not visible in the output.

        Parameters
        ----------
        minor : bool, default: False
            True to return the minor tick directions,
            False to return the major tick directions.

        Returns
        -------
        numpy array of tick locations
        """
        return self.get_minorticklocs() if minor else self.get_majorticklocs()
