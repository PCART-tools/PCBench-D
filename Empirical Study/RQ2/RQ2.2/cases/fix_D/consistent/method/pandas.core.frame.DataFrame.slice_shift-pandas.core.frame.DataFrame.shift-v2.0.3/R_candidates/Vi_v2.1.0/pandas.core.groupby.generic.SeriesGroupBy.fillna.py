    def fillna(
        self,
        value: object | ArrayLike | None = None,
        method: FillnaOptions | None = None,
        axis: Axis | None | lib.NoDefault = lib.no_default,
        inplace: bool = False,
        limit: int | None = None,
        downcast: dict | None | lib.NoDefault = lib.no_default,
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

            .. deprecated:: 2.1.0
                Use obj.ffill or obj.bfill instead.

        axis : {0 or 'index', 1 or 'columns'}
            Unused, only for compatibility with :meth:`DataFrameGroupBy.fillna`.

            .. deprecated:: 2.1.0
                For axis=1, operate on the underlying object instead. Otherwise
                the axis keyword is not necessary.

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

            .. deprecated:: 2.1.0

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
        For SeriesGroupBy:

        >>> lst = ['cat', 'cat', 'cat', 'mouse', 'mouse']
        >>> ser = pd.Series([1, None, None, 2, None], index=lst)
        >>> ser
        cat    1.0
        cat    NaN
        cat    NaN
        mouse  2.0
        mouse  NaN
        dtype: float64
        >>> ser.groupby(level=0).fillna(0, limit=1)
        cat    1.0
        cat    0.0
        cat    NaN
        mouse  2.0
        mouse  0.0
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
