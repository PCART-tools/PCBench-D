    @property
    def ftypes(self):
        """
        Return the ftypes (indication of sparse/dense and dtype) in DataFrame.

        .. deprecated:: 0.25.0
           Use :func:`dtypes` instead.

        This returns a Series with the data type of each column.
        The result's index is the original DataFrame's columns. Columns
        with mixed types are stored with the ``object`` dtype.  See
        :ref:`the User Guide <basics.dtypes>` for more.

        Returns
        -------
        pandas.Series
            The data type and indication of sparse/dense of each column.

        See Also
        --------
        DataFrame.dtypes: Series with just dtype information.
        SparseDataFrame : Container for sparse tabular data.

        Notes
        -----
        Sparse data should have the same dtypes as its dense representation.

        Examples
        --------
        >>> arr = np.random.RandomState(0).randn(100, 4)
        >>> arr[arr < .8] = np.nan
        >>> pd.DataFrame(arr).ftypes
        0    float64:dense
        1    float64:dense
        2    float64:dense
        3    float64:dense
        dtype: object

        >>> pd.SparseDataFrame(arr).ftypes  # doctest: +SKIP
        0    float64:sparse
        1    float64:sparse
        2    float64:sparse
        3    float64:sparse
        dtype: object
        """
        warnings.warn(
            "DataFrame.ftypes is deprecated and will "
            "be removed in a future version. "
            "Use DataFrame.dtypes instead.",
            FutureWarning,
            stacklevel=2,
        )

        from pandas import Series

        return Series(self._data.get_ftypes(), index=self._info_axis, dtype=np.object_)
