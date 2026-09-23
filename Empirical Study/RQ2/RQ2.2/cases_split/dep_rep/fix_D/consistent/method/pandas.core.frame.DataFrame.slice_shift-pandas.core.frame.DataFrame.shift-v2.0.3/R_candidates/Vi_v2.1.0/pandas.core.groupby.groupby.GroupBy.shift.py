    @final
    @Substitution(name="groupby")
    def shift(
        self,
        periods: int | Sequence[int] = 1,
        freq=None,
        axis: Axis | lib.NoDefault = lib.no_default,
        fill_value=lib.no_default,
        suffix: str | None = None,
    ):
        """
        Shift each group by periods observations.

        If freq is passed, the index will be increased using the periods and the freq.

        Parameters
        ----------
        periods : int | Sequence[int], default 1
            Number of periods to shift. If a list of values, shift each group by
            each period.
        freq : str, optional
            Frequency string.
        axis : axis to shift, default 0
            Shift direction.

            .. deprecated:: 2.1.0
                For axis=1, operate on the underlying object instead. Otherwise
                the axis keyword is not necessary.

        fill_value : optional
            The scalar value to use for newly introduced missing values.

            .. versionchanged:: 2.1.0
                Will raise a ``ValueError`` if ``freq`` is provided too.

        suffix : str, optional
            A string to add to each shifted column if there are multiple periods.
            Ignored otherwise.

        Returns
        -------
        Series or DataFrame
            Object shifted within each group.

        See Also
        --------
        Index.shift : Shift values of Index.

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
        >>> ser.groupby(level=0).shift(1)
        a    NaN
        a    1.0
        b    NaN
        b    3.0
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
        >>> df.groupby("a").shift(1)
                      b    c
            tuna    NaN  NaN
          salmon    2.0  3.0
         catfish    NaN  NaN
        goldfish    5.0  8.0
        """
        if axis is not lib.no_default:
            axis = self.obj._get_axis_number(axis)
            self._deprecate_axis(axis, "shift")
        else:
            axis = 0

        if is_list_like(periods):
            if axis == 1:
                raise ValueError(
                    "If `periods` contains multiple shifts, `axis` cannot be 1."
                )
            periods = cast(Sequence, periods)
            if len(periods) == 0:
                raise ValueError("If `periods` is an iterable, it cannot be empty.")
            from pandas.core.reshape.concat import concat

            add_suffix = True
        else:
            if not is_integer(periods):
                raise TypeError(
                    f"Periods must be integer, but {periods} is {type(periods)}."
                )
            if suffix:
                raise ValueError("Cannot specify `suffix` if `periods` is an int.")
            periods = [cast(int, periods)]
            add_suffix = False

        shifted_dataframes = []
        for period in periods:
            if not is_integer(period):
                raise TypeError(
                    f"Periods must be integer, but {period} is {type(period)}."
                )
            period = cast(int, period)
            if freq is not None or axis != 0:
                f = lambda x: x.shift(
                    period, freq, axis, fill_value  # pylint: disable=cell-var-from-loop
                )
                shifted = self._python_apply_general(
                    f, self._selected_obj, is_transform=True
                )
            else:
                if fill_value is lib.no_default:
                    fill_value = None
                ids, _, ngroups = self.grouper.group_info
                res_indexer = np.zeros(len(ids), dtype=np.int64)

                libgroupby.group_shift_indexer(res_indexer, ids, ngroups, period)

                obj = self._obj_with_exclusions

                shifted = obj._reindex_with_indexers(
                    {self.axis: (obj.axes[self.axis], res_indexer)},
                    fill_value=fill_value,
                    allow_dups=True,
                )

            if add_suffix:
                if isinstance(shifted, Series):
                    shifted = cast(NDFrameT, shifted.to_frame())
                shifted = shifted.add_suffix(
                    f"{suffix}_{period}" if suffix else f"_{period}"
                )
            shifted_dataframes.append(cast(Union[Series, DataFrame], shifted))

        return (
            shifted_dataframes[0]
            if len(shifted_dataframes) == 1
            else concat(shifted_dataframes, axis=1)
        )
