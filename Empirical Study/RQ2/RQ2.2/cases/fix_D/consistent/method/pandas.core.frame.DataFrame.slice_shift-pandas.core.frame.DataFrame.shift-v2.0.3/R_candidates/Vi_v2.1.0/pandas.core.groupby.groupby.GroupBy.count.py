    @final
    @Substitution(name="groupby")
    @Substitution(see_also=_common_see_also)
    def count(self) -> NDFrameT:
        """
        Compute count of group, excluding missing values.

        Returns
        -------
        Series or DataFrame
            Count of values within each group.
        %(see_also)s
        Examples
        --------
        For SeriesGroupBy:

        >>> lst = ['a', 'a', 'b']
        >>> ser = pd.Series([1, 2, np.nan], index=lst)
        >>> ser
        a    1.0
        a    2.0
        b    NaN
        dtype: float64
        >>> ser.groupby(level=0).count()
        a    2
        b    0
        dtype: int64

        For DataFrameGroupBy:

        >>> data = [[1, np.nan, 3], [1, np.nan, 6], [7, 8, 9]]
        >>> df = pd.DataFrame(data, columns=["a", "b", "c"],
        ...                   index=["cow", "horse", "bull"])
        >>> df
                a	  b	c
        cow     1	NaN	3
        horse	1	NaN	6
        bull	7	8.0	9
        >>> df.groupby("a").count()
            b   c
        a
        1   0   2
        7   1   1

        For Resampler:

        >>> ser = pd.Series([1, 2, 3, 4], index=pd.DatetimeIndex(
        ...                 ['2023-01-01', '2023-01-15', '2023-02-01', '2023-02-15']))
        >>> ser
        2023-01-01    1
        2023-01-15    2
        2023-02-01    3
        2023-02-15    4
        dtype: int64
        >>> ser.resample('MS').count()
        2023-01-01    2
        2023-02-01    2
        Freq: MS, dtype: int64
        """
        data = self._get_data_to_aggregate()
        ids, _, ngroups = self.grouper.group_info
        mask = ids != -1

        is_series = data.ndim == 1

        def hfunc(bvalues: ArrayLike) -> ArrayLike:
            # TODO(EA2D): reshape would not be necessary with 2D EAs
            if bvalues.ndim == 1:
                # EA
                masked = mask & ~isna(bvalues).reshape(1, -1)
            else:
                masked = mask & ~isna(bvalues)

            counted = lib.count_level_2d(masked, labels=ids, max_bin=ngroups)
            if isinstance(bvalues, BaseMaskedArray):
                return IntegerArray(
                    counted[0], mask=np.zeros(counted.shape[1], dtype=np.bool_)
                )
            elif isinstance(bvalues, ArrowExtensionArray) and not isinstance(
                bvalues.dtype, StringDtype
            ):
                return type(bvalues)._from_sequence(counted[0])
            if is_series:
                assert counted.ndim == 2
                assert counted.shape[0] == 1
                return counted[0]
            return counted

        new_mgr = data.grouped_reduce(hfunc)
        new_obj = self._wrap_agged_manager(new_mgr)

        # If we are grouping on categoricals we want unobserved categories to
        # return zero, rather than the default of NaN which the reindexing in
        # _wrap_aggregated_output() returns. GH 35028
        # e.g. test_dataframe_groupby_on_2_categoricals_when_observed_is_false
        with com.temp_setattr(self, "observed", True):
            result = self._wrap_aggregated_output(new_obj)

        return self._reindex_output(result, fill_value=0)
