    def argmax(self, axis=None, skipna=True, *args, **kwargs):
        """
        Return an ndarray of the maximum argument indexer.

        Parameters
        ----------
        axis : {None}
            Dummy argument for consistency with Series
        skipna : bool, default True

        Returns
        -------
        numpy.ndarray
            Indices of the maximum values.

        See Also
        --------
        numpy.ndarray.argmax
        """
        nv.validate_minmax_axis(axis)
        nv.validate_argmax_with_skipna(skipna, args, kwargs)
        return nanops.nanargmax(self._values, skipna=skipna)
