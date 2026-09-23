    def argmin(self, axis=None, skipna=True, *args, **kwargs):
        """
        Return a ndarray of the minimum argument indexer.

        Parameters
        ----------
        axis : {None}
            Dummy argument for consistency with Series.
        skipna : bool, default True

        Returns
        -------
        numpy.ndarray

        See Also
        --------
        numpy.ndarray.argmin
        """
        nv.validate_minmax_axis(axis)
        nv.validate_argmax_with_skipna(skipna, args, kwargs)
        return nanops.nanargmin(self._values, skipna=skipna)
