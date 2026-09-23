    def fillna(
        self,
        value: Hashable | Mapping | Series | DataFrame = None,
        method: FillnaOptions | None = None,
        axis: Axis | None = None,
        inplace: bool = False,
        limit=None,
        downcast=None,
    ) -> DataFrame | None:
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
            should prefer :meth:`.DataFrame.fillna` as this
            will produce the same result and be more performant.
        method : {{'bfill', 'ffill', None}}, default None
            Method to use for filling holes. ``'ffill'`` will propagate
            the last valid observation forward within a group.
            ``'bfill'`` will use next valid observation to fill the gap.
        axis : {0 or 'index', 1 or 'columns'}
            Axis along which to fill missing values. When the :class:`DataFrameGroupBy`
            ``axis`` argument is ``0``, using ``axis=1`` here will produce
            the same results as :meth:`.DataFrame.fillna`. When the
            :class:`DataFrameGroupBy` ``axis`` argument is ``1``, using ``axis=0``
            or ``axis=1`` here will produce the same results.
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
        DataFrame
            Object with missing values filled.

        See Also
        --------
        ffill : Forward fill values within a group.
        bfill : Backward fill values within a group.

        Examples
        --------
        >>> df = pd.DataFrame(
        ...     {
        ...         "key": [0, 0, 1, 1, 1],
        ...         "A": [np.nan, 2, np.nan, 3, np.nan],
        ...         "B": [2, 3, np.nan, np.nan, np.nan],
        ...         "C": [np.nan, np.nan, 2, np.nan, np.nan],
        ...     }
        ... )
        >>> df
           key    A    B   C
        0    0  NaN  2.0 NaN
        1    0  2.0  3.0 NaN
        2    1  NaN  NaN 2.0
        3    1  3.0  NaN NaN
        4    1  NaN  NaN NaN

        Propagate non-null values forward or backward within each group along columns.

        >>> df.groupby("key").fillna(method="ffill")
             A    B   C
        0  NaN  2.0 NaN
        1  2.0  3.0 NaN
        2  NaN  NaN 2.0
        3  3.0  NaN 2.0
        4  3.0  NaN 2.0

        >>> df.groupby("key").fillna(method="bfill")
             A    B   C
        0  2.0  2.0 NaN
        1  2.0  3.0 NaN
        2  3.0  NaN 2.0
        3  3.0  NaN NaN
        4  NaN  NaN NaN

        Propagate non-null values forward or backward within each group along rows.

        >>> df.groupby([0, 0, 1, 1], axis=1).fillna(method="ffill")
           key    A    B    C
        0  0.0  0.0  2.0  2.0
        1  0.0  2.0  3.0  3.0
        2  1.0  1.0  NaN  2.0
        3  1.0  3.0  NaN  NaN
        4  1.0  1.0  NaN  NaN

        >>> df.groupby([0, 0, 1, 1], axis=1).fillna(method="bfill")
           key    A    B    C
        0  0.0  NaN  2.0  NaN
        1  0.0  2.0  3.0  NaN
        2  1.0  NaN  2.0  2.0
        3  1.0  3.0  NaN  NaN
        4  1.0  NaN  NaN  NaN

        Only replace the first NaN element within a group along rows.

        >>> df.groupby("key").fillna(method="ffill", limit=1)
             A    B    C
        0  NaN  2.0  NaN
        1  2.0  3.0  NaN
        2  NaN  NaN  2.0
        3  3.0  NaN  2.0
        4  3.0  NaN  NaN
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
