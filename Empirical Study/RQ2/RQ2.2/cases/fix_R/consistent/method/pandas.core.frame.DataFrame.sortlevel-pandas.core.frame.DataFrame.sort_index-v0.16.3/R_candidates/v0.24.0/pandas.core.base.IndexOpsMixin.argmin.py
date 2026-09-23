    def argmin(self, axis=None, skipna=True):
        """
        Return a ndarray of the minimum argument indexer.

        Parameters
        ----------
        axis : {None}
            Dummy argument for consistency with Series
        skipna : bool, default True

        See Also
        --------
        numpy.ndarray.argmin
        """
        nv.validate_minmax_axis(axis)
        return nanops.nanargmin(self._values, skipna=skipna)
