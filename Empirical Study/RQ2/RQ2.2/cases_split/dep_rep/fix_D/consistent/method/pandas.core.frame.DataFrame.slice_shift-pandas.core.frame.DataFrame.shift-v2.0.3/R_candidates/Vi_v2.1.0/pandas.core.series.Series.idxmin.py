    def idxmin(self, axis: Axis = 0, skipna: bool = True, *args, **kwargs) -> Hashable:
        """
        Return the row label of the minimum value.

        If multiple values equal the minimum, the first row label with that
        value is returned.

        Parameters
        ----------
        axis : {0 or 'index'}
            Unused. Parameter needed for compatibility with DataFrame.
        skipna : bool, default True
            Exclude NA/null values. If the entire Series is NA, the result
            will be NA.
        *args, **kwargs
            Additional arguments and keywords have no effect but might be
            accepted for compatibility with NumPy.

        Returns
        -------
        Index
            Label of the minimum value.

        Raises
        ------
        ValueError
            If the Series is empty.

        See Also
        --------
        numpy.argmin : Return indices of the minimum values
            along the given axis.
        DataFrame.idxmin : Return index of first occurrence of minimum
            over requested axis.
        Series.idxmax : Return index *label* of the first occurrence
            of maximum of values.

        Notes
        -----
        This method is the Series version of ``ndarray.argmin``. This method
        returns the label of the minimum, while ``ndarray.argmin`` returns
        the position. To get the position, use ``series.values.argmin()``.

        Examples
        --------
        >>> s = pd.Series(data=[1, None, 4, 1],
        ...               index=['A', 'B', 'C', 'D'])
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
        axis = self._get_axis_number(axis)
        with warnings.catch_warnings():
            # TODO(3.0): this catching/filtering can be removed
            # ignore warning produced by argmin since we will issue a different
            #  warning for idxmin
            warnings.simplefilter("ignore")
            i = self.argmin(axis, skipna, *args, **kwargs)

        if i == -1:
            # GH#43587 give correct NA value for Index.
            warnings.warn(
                f"The behavior of {type(self).__name__}.idxmin with all-NA "
                "values, or any-NA and skipna=False, is deprecated. In a future "
                "version this will raise ValueError",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
            return self.index._na_value
        return self.index[i]
