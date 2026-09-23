    def argmax(self, axis=None, skipna=True):
        """
        Return a ndarray of the maximum argument indexer.

        Parameters
        ----------
        axis : {None}
            Dummy argument for consistency with Series
        skipna : bool, default True

        See Also
        --------
        numpy.ndarray.argmax
        """
        nv.validate_minmax_axis(axis)
        return nanops.nanargmax(self._values, skipna=skipna)
