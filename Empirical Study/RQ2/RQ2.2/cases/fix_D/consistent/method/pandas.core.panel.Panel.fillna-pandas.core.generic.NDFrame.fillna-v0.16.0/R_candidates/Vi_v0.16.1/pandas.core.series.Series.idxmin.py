    def idxmin(self, axis=None, out=None, skipna=True):
        """
        Index of first occurrence of minimum of values.

        Parameters
        ----------
        skipna : boolean, default True
            Exclude NA/null values

        Returns
        -------
        idxmin : Index of minimum of values

        Notes
        -----
        This method is the Series version of ``ndarray.argmin``.

        See Also
        --------
        DataFrame.idxmin
        numpy.ndarray.argmin
        """
        i = nanops.nanargmin(_values_from_object(self), skipna=skipna)
        if i == -1:
            return np.nan
        return self.index[i]
