    def idxmin(self, axis=None, skipna=True, *args, **kwargs):
        """
        Return the row label of the minimum value.

        If multiple values equal the minimum, the first row label with that
        value is returned.

        Parameters
        ----------
        skipna : boolean, default True
            Exclude NA/null values. If the entire Series is NA, the result
            will be NA.
        axis : int, default 0
            For compatibility with DataFrame.idxmin. Redundant for application
            on Series.
        *args, **kwargs
            Additional keywors have no effect but might be accepted
            for compatibility with NumPy.

        Returns
        -------
        idxmin : Index of minimum of values.

        Raises
        ------
        ValueError
            If the Series is empty.

        Notes
        -----
        This method is the Series version of ``ndarray.argmin``. This method
        returns the label of the minimum, while ``ndarray.argmin`` returns
        the position. To get the position, use ``series.values.argmin()``.

        See Also
        --------
        numpy.argmin : Return indices of the minimum values
            along the given axis.
        DataFrame.idxmin : Return index of first occurrence of minimum
            over requested axis.
        Series.idxmax : Return index *label* of the first occurrence
            of maximum of values.

        Examples
        --------
        >>> s = pd.Series(data=[1, None, 4, 1],
        ...               index=['A' ,'B' ,'C' ,'D'])
        >>> s
        A    1.0
        B    NaN
        C    4.0
        D    1.0
        dtype: float64

        >>> s.idxmin()
        'A'

        If `skipna` is False and there is an NA value in the data,
        the function returns ``nan``.

        >>> s.idxmin(skipna=False)
        nan
        """
        skipna = nv.validate_argmin_with_skipna(skipna, args, kwargs)
        i = nanops.nanargmin(com._values_from_object(self), skipna=skipna)
        if i == -1:
            return np.nan
        return self.index[i]
