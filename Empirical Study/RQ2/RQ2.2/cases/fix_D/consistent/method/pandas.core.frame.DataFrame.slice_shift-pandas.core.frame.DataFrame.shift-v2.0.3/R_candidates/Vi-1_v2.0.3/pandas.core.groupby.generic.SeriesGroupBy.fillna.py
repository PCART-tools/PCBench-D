    def fillna(
        self,
        value: object | ArrayLike | None = None,
        method: FillnaOptions | None = None,
        axis: Axis | None = None,
        inplace: bool = False,
        limit: int | None = None,
        downcast: dict | None = None,
    ) -> Series | None:
        """
        Fill NA/NaN values using the specified method within groups.

        Parameters
        ----------
        value : scalar, dict, Series, or DataFrame
            Value to use to fill holes (e.g. 0), alternately a
            dict/Series/DataFrame of values specifying which value to use for
            each index (for a Series) or column (for a DataFrame).  Values not
            in the dict/Series/DataFrame will not be filled. This value cannot
            be a list. Users wanting to use the ``value`` argument and not ``method``
            should prefer :meth:`.Series.fillna` as this
            will produce the same result and be more performant.
        method : {{'bfill', 'ffill', None}}, default None
            Method to use for filling holes. ``'ffill'`` will propagate
            the last valid observation forward within a group.
            ``'bfill'`` will use next valid observation to fill the gap.
        axis : {0 or 'index', 1 or 'columns'}
            Unused, only for compatibility with :meth:`DataFrameGroupBy.fillna`.
        inplace : bool, default False
            Broken. Do not set to True.
        limit : int, default None
            If method is specified, this is the maximum number of consecutive
            NaN values to forward/backward fill within a group. In other words,
            if there is a gap with more than this number of consecutive NaNs,
            it will only be partially filled. If method is not specified, this is the
            maximum number of entries along the entire axis where NaNs will be
            filled. Must be greater than 0 if not None.
        downcast : dict, default is None
            A dict of item->dtype of what to downcast if possible,
            or the string 'infer' which will try to downcast to an appropriate
            equal type (e.g. float64 to int64 if possible).

        Returns
        -------
        Series
            Object with missing values filled within groups.

        See Also
        --------
        ffill : Forward fill values within a group.
        bfill : Backward fill values within a group.

        Examples
        --------
        >>> ser = pd.Series([np.nan, np.nan, 2, 3, np.nan, np.nan])
        >>> ser
        0    NaN
        1    NaN
        2    2.0
        3    3.0
        4    NaN
        5    NaN
        dtype: float64

        Propagate non-null values forward or backward within each group.

        >>> ser.groupby([0, 0, 0, 1, 1, 1]).fillna(method="ffill")
        0    NaN
        1    NaN
        2    2.0
        3    3.0
        4    3.0
        5    3.0
        dtype: float64

        >>> ser.groupby([0, 0, 0, 1, 1, 1]).fillna(method="bfill")
        0    2.0
        1    2.0
        2    2.0
        3    3.0
        4    NaN
        5    NaN
        dtype: float64

        Only replace the first NaN element within a group.

        >>> ser.groupby([0, 0, 0, 1, 1, 1]).fillna(method="ffill", limit=1)
        0    NaN
        1    NaN
        2    2.0
        3    3.0
        4    3.0
        5    NaN
        dtype: float64
        """
        result = self._op_via_apply(
            "fillna",
            value=value,
            method=method,
            axis=axis,
            inplace=inplace,
            limit=limit,
            downcast=downcast,
        )
        return result
