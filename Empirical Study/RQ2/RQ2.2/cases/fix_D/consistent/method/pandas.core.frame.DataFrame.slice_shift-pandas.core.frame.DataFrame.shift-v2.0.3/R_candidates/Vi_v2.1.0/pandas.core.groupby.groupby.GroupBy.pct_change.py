    @final
    @Substitution(name="groupby")
    @Substitution(see_also=_common_see_also)
    def pct_change(
        self,
        periods: int = 1,
        fill_method: FillnaOptions | lib.NoDefault = lib.no_default,
        limit: int | None | lib.NoDefault = lib.no_default,
        freq=None,
        axis: Axis | lib.NoDefault = lib.no_default,
    ):
        """
        Calculate pct_change of each value to previous entry in group.

        Returns
        -------
        Series or DataFrame
            Percentage changes within each group.
        %(see_also)s
        Examples
        --------

        For SeriesGroupBy:

        >>> lst = ['a', 'a', 'b', 'b']
        >>> ser = pd.Series([1, 2, 3, 4], index=lst)
        >>> ser
        a    1
        a    2
        b    3
        b    4
        dtype: int64
        >>> ser.groupby(level=0).pct_change()
        a         NaN
        a    1.000000
        b         NaN
        b    0.333333
        dtype: float64

        For DataFrameGroupBy:

        >>> data = [[1, 2, 3], [1, 5, 6], [2, 5, 8], [2, 6, 9]]
        >>> df = pd.DataFrame(data, columns=["a", "b", "c"],
        ...                   index=["tuna", "salmon", "catfish", "goldfish"])
        >>> df
                   a  b  c
            tuna   1  2  3
          salmon   1  5  6
         catfish   2  5  8
        goldfish   2  6  9
        >>> df.groupby("a").pct_change()
                    b  c
            tuna    NaN    NaN
          salmon    1.5  1.000
         catfish    NaN    NaN
        goldfish    0.2  0.125
        """
        # GH#53491
        if fill_method is not lib.no_default or limit is not lib.no_default:
            warnings.warn(
                "The 'fill_method' and 'limit' keywords in "
                f"{type(self).__name__}.pct_change are deprecated and will be "
                "removed in a future version. Call "
                f"{'bfill' if fill_method in ('backfill', 'bfill') else 'ffill'} "
                "before calling pct_change instead.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
        if fill_method is lib.no_default:
            if any(grp.isna().values.any() for _, grp in self):
                warnings.warn(
                    "The default fill_method='ffill' in "
                    f"{type(self).__name__}.pct_change is deprecated and will be "
                    "removed in a future version. Call ffill before calling "
                    "pct_change to retain current behavior and silence this warning.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
            fill_method = "ffill"
        if limit is lib.no_default:
            limit = None

        if axis is not lib.no_default:
            axis = self.obj._get_axis_number(axis)
            self._deprecate_axis(axis, "pct_change")
        else:
            axis = 0

        # TODO(GH#23918): Remove this conditional for SeriesGroupBy when
        #  GH#23918 is fixed
        if freq is not None or axis != 0:
            f = lambda x: x.pct_change(
                periods=periods,
                fill_method=fill_method,
                limit=limit,
                freq=freq,
                axis=axis,
            )
            return self._python_apply_general(f, self._selected_obj, is_transform=True)

        if fill_method is None:  # GH30463
            fill_method = "ffill"
            limit = 0
        filled = getattr(self, fill_method)(limit=limit)
        if self.axis == 0:
            fill_grp = filled.groupby(self.grouper.codes, group_keys=self.group_keys)
        else:
            fill_grp = filled.T.groupby(self.grouper.codes, group_keys=self.group_keys)
        shifted = fill_grp.shift(periods=periods, freq=freq)
        if self.axis == 1:
            shifted = shifted.T
        return (filled / shifted) - 1
