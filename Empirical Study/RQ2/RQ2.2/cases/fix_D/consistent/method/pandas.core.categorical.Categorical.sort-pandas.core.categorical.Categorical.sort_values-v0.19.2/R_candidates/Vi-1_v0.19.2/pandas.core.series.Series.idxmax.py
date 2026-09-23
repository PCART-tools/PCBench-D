    def idxmax(self, axis=None, skipna=True, *args, **kwargs):
        """
        Index of first occurrence of maximum of values.

        Parameters
        ----------
        skipna : boolean, default True
            Exclude NA/null values

        Returns
        -------
        idxmax : Index of maximum of values

        Notes
        -----
        This method is the Series version of ``ndarray.argmax``.

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
