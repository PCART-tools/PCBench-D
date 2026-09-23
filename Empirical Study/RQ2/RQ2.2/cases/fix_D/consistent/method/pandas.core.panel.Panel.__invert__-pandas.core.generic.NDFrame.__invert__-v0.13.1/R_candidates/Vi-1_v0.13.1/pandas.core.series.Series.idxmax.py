    def idxmax(self, axis=None, out=None, skipna=True):
        """
        Index of first occurrence of maximum of values.

        Parameters
        ----------
        skipna : boolean, default True
            Exclude NA/null values

        Returns
        -------
        idxmax : Index of minimum of values

        Notes
        -----
        This method is the Series version of ``ndarray.argmax``.

        See Also
        --------
        DataFrame.idxmax
        """
        i = nanops.nanargmax(_values_from_object(self), skipna=skipna)
        if i == -1:
            return pa.NA
        return self.index[i]
