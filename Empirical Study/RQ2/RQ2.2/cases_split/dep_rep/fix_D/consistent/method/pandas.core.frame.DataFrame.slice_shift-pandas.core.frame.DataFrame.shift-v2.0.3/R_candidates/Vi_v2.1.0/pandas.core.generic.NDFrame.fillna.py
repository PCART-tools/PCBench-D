    @final
    @doc(
        klass=_shared_doc_kwargs["klass"],
        axes_single_arg=_shared_doc_kwargs["axes_single_arg"],
    )
    def fillna(
        self,
        value: Hashable | Mapping | Series | DataFrame | None = None,
        *,
        method: FillnaOptions | None = None,
        axis: Axis | None = None,
        inplace: bool_t = False,
        limit: int | None = None,
        downcast: dict | None | lib.NoDefault = lib.no_default,
    ) -> Self | None:
        """
        Fill NA/NaN values using the specified method.

        Parameters
        ----------
        value : scalar, dict, Series, or DataFrame
            Value to use to fill holes (e.g. 0), alternately a
            dict/Series/DataFrame of values specifying which value to use for
            each index (for a Series) or column (for a DataFrame).  Values not
            in the dict/Series/DataFrame will not be filled. This value cannot
            be a list.
        method : {{'backfill', 'bfill', 'ffill', None}}, default None
            Method to use for filling holes in reindexed Series:

            * ffill: propagate last valid observation forward to next valid.
            * backfill / bfill: use next valid observation to fill gap.

            .. deprecated:: 2.1.0
                Use ffill or bfill instead.

        axis : {axes_single_arg}
            Axis along which to fill missing values. For `Series`
            this parameter is unused and defaults to 0.
        inplace : bool, default False
            If True, fill in-place. Note: this will modify any
            other views on this object (e.g., a no-copy slice for a column in a
            DataFrame).
        limit : int, default None
            If method is specified, this is the maximum number of consecutive
            NaN values to forward/backward fill. In other words, if there is
            a gap with more than this number of consecutive NaNs, it will only
            be partially filled. If method is not specified, this is the
            maximum number of entries along the entire axis where NaNs will be
            filled. Must be greater than 0 if not None.
        downcast : dict, default is None
            A dict of item->dtype of what to downcast if possible,
            or the string 'infer' which will try to downcast to an appropriate
            equal type (e.g. float64 to int64 if possible).

        Returns
        -------
        {klass} or None
            Object with missing values filled or None if ``inplace=True``.

        See Also
        --------
        ffill : Fill values by propagating the last valid observation to next valid.
        bfill : Fill values by using the next valid observation to fill the gap.
        interpolate : Fill NaN values using interpolation.
        reindex : Conform object to new index.
        asfreq : Convert TimeSeries to specified frequency.

        Examples
        --------
        >>> df = pd.DataFrame([[np.nan, 2, np.nan, 0],
        ...                    [3, 4, np.nan, 1],
        ...                    [np.nan, np.nan, np.nan, np.nan],
        ...                    [np.nan, 3, np.nan, 4]],
        ...                   columns=list("ABCD"))
        >>> df
             A    B   C    D
        0  NaN  2.0 NaN  0.0
        1  3.0  4.0 NaN  1.0
        2  NaN  NaN NaN  NaN
        3  NaN  3.0 NaN  4.0

        Replace all NaN elements with 0s.

        >>> df.fillna(0)
             A    B    C    D
        0  0.0  2.0  0.0  0.0
        1  3.0  4.0  0.0  1.0
        2  0.0  0.0  0.0  0.0
        3  0.0  3.0  0.0  4.0

        Replace all NaN elements in column 'A', 'B', 'C', and 'D', with 0, 1,
        2, and 3 respectively.

        >>> values = {{"A": 0, "B": 1, "C": 2, "D": 3}}
        >>> df.fillna(value=values)
             A    B    C    D
        0  0.0  2.0  2.0  0.0
        1  3.0  4.0  2.0  1.0
        2  0.0  1.0  2.0  3.0
        3  0.0  3.0  2.0  4.0

        Only replace the first NaN element.

        >>> df.fillna(value=values, limit=1)
             A    B    C    D
        0  0.0  2.0  2.0  0.0
        1  3.0  4.0  NaN  1.0
        2  NaN  1.0  NaN  3.0
        3  NaN  3.0  NaN  4.0

        When filling using a DataFrame, replacement happens along
        the same column names and same indices

        >>> df2 = pd.DataFrame(np.zeros((4, 4)), columns=list("ABCE"))
        >>> df.fillna(df2)
             A    B    C    D
        0  0.0  2.0  0.0  0.0
        1  3.0  4.0  0.0  1.0
        2  0.0  0.0  0.0  NaN
        3  0.0  3.0  0.0  4.0

        Note that column D is not affected since it is not present in df2.
        """
        inplace = validate_bool_kwarg(inplace, "inplace")
        if inplace:
            if not PYPY and using_copy_on_write():
                if sys.getrefcount(self) <= REF_COUNT:
                    warnings.warn(
                        _chained_assignment_method_msg,
                        ChainedAssignmentError,
                        stacklevel=2,
                    )

        value, method = validate_fillna_kwargs(value, method)
        if method is not None:
            warnings.warn(
                f"{type(self).__name__}.fillna with 'method' is deprecated and "
                "will raise in a future version. Use obj.ffill() or obj.bfill() "
                "instead.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )

        was_no_default = downcast is lib.no_default
        downcast = self._deprecate_downcast(downcast, "fillna")

        # set the default here, so functions examining the signaure
        # can detect if something was set (e.g. in groupby) (GH9221)
        if axis is None:
            axis = 0
        axis = self._get_axis_number(axis)

        if value is None:
            return self._pad_or_backfill(
                # error: Argument 1 to "_pad_or_backfill" of "NDFrame" has
                # incompatible type "Optional[Literal['backfill', 'bfill', 'ffill',
                # 'pad']]"; expected "Literal['ffill', 'bfill', 'pad', 'backfill']"
                method,  # type: ignore[arg-type]
                axis=axis,
                limit=limit,
                inplace=inplace,
                # error: Argument "downcast" to "_fillna_with_method" of "NDFrame"
                # has incompatible type "Union[Dict[Any, Any], None,
                # Literal[_NoDefault.no_default]]"; expected
                # "Optional[Dict[Any, Any]]"
                downcast=downcast,  # type: ignore[arg-type]
            )
        else:
            if self.ndim == 1:
                if isinstance(value, (dict, ABCSeries)):
                    if not len(value):
                        # test_fillna_nonscalar
                        if inplace:
                            return None
                        return self.copy(deep=None)
                    from pandas import Series

                    value = Series(value)
                    value = value.reindex(self.index, copy=False)
                    value = value._values
                elif not is_list_like(value):
                    pass
                else:
                    raise TypeError(
                        '"value" parameter must be a scalar, dict '
                        "or Series, but you passed a "
                        f'"{type(value).__name__}"'
                    )

                new_data = self._mgr.fillna(
                    value=value, limit=limit, inplace=inplace, downcast=downcast
                )

            elif isinstance(value, (dict, ABCSeries)):
                if axis == 1:
                    raise NotImplementedError(
                        "Currently only can fill "
                        "with dict/Series column "
                        "by column"
                    )
                if using_copy_on_write():
                    result = self.copy(deep=None)
                else:
                    result = self if inplace else self.copy()
                is_dict = isinstance(downcast, dict)
                for k, v in value.items():
                    if k not in result:
                        continue

                    if was_no_default:
                        downcast_k = lib.no_default
                    else:
                        downcast_k = (
                            # error: Incompatible types in assignment (expression
                            # has type "Union[Dict[Any, Any], None,
                            # Literal[_NoDefault.no_default], Any]", variable has
                            # type "_NoDefault")
                            downcast  # type: ignore[assignment]
                            if not is_dict
                            # error: Item "None" of "Optional[Dict[Any, Any]]" has
                            # no attribute "get"
                            else downcast.get(k)  # type: ignore[union-attr]
                        )

                    res_k = result[k].fillna(v, limit=limit, downcast=downcast_k)

                    if not inplace:
                        result[k] = res_k
                    else:
                        # We can write into our existing column(s) iff dtype
                        #  was preserved.
                        if isinstance(res_k, ABCSeries):
                            # i.e. 'k' only shows up once in self.columns
                            if res_k.dtype == result[k].dtype:
                                result.loc[:, k] = res_k
                            else:
                                # Different dtype -> no way to do inplace.
                                result[k] = res_k
                        else:
                            # see test_fillna_dict_inplace_nonunique_columns
                            locs = result.columns.get_loc(k)
                            if isinstance(locs, slice):
                                locs = np.arange(self.shape[1])[locs]
                            elif (
                                isinstance(locs, np.ndarray) and locs.dtype.kind == "b"
                            ):
                                locs = locs.nonzero()[0]
                            elif not (
                                isinstance(locs, np.ndarray) and locs.dtype.kind == "i"
                            ):
                                # Should never be reached, but let's cover our bases
                                raise NotImplementedError(
                                    "Unexpected get_loc result, please report a bug at "
                                    "https://github.com/pandas-dev/pandas"
                                )

                            for i, loc in enumerate(locs):
                                res_loc = res_k.iloc[:, i]
                                target = self.iloc[:, loc]

                                if res_loc.dtype == target.dtype:
                                    result.iloc[:, loc] = res_loc
                                else:
                                    result.isetitem(loc, res_loc)
                if inplace:
                    return self._update_inplace(result)
                else:
                    return result

            elif not is_list_like(value):
                if axis == 1:
                    result = self.T.fillna(value=value, limit=limit).T
                    new_data = result._mgr
                else:
                    new_data = self._mgr.fillna(
                        value=value, limit=limit, inplace=inplace, downcast=downcast
                    )
            elif isinstance(value, ABCDataFrame) and self.ndim == 2:
                new_data = self.where(self.notna(), value)._mgr
            else:
                raise ValueError(f"invalid fill value with a {type(value)}")

        result = self._constructor_from_mgr(new_data, axes=new_data.axes)
        if inplace:
            return self._update_inplace(result)
        else:
            return result.__finalize__(self, method="fillna")
