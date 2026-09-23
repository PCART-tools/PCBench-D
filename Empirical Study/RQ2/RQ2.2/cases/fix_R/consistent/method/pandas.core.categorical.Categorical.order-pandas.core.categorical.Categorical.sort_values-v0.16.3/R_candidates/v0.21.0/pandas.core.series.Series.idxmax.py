    def idxmax(self, axis=None, skipna=True, *args, **kwargs):
        """
        Index *label* of the first occurrence of maximum of values.

        Parameters
        ----------
        skipna : boolean, default True
            Exclude NA/null values

        Returns
        -------
        idxmax : Index of maximum of values

        Notes
        -----
        This method is the Series version of ``ndarray.argmax``. This method
        returns the label of the maximum, while ``ndarray.argmax`` returns
        the position. To get the position, use ``series.values.argmax()``.

        See Also
        --------
        DataFrame.idxmax
        numpy.ndarray.argmax
        """
        skipna = nv.validate_argmax_with_skipna(skipna, args, kwargs)
        i = nanops.nanargmax(_values_from_object(self), skipna=skipna)
        if i == -1:
            return np.nan
        return self.index[i]
