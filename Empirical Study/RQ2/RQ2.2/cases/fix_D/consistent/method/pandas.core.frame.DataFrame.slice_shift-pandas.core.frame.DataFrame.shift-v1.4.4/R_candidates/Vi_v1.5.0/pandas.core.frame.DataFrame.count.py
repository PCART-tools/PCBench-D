    def count(self, axis: Axis = 0, level: Level = None, numeric_only: bool = False):
        """
        Count non-NA cells for each column or row.

        The values `None`, `NaN`, `NaT`, and optionally `numpy.inf` (depending
        on `pandas.options.mode.use_inf_as_na`) are considered NA.

        Parameters
        ----------
        axis : {0 or 'index', 1 or 'columns'}, default 0
            If 0 or 'index' counts are generated for each column.
            If 1 or 'columns' counts are generated for each row.
        level : int or str, optional
            If the axis is a `MultiIndex` (hierarchical), count along a
            particular `level`, collapsing into a `DataFrame`.
            A `str` specifies the level name.
        numeric_only : bool, default False
            Include only `float`, `int` or `boolean` data.

        Returns
        -------
        Series or DataFrame
            For each column/row the number of non-NA/null entries.
            If `level` is specified returns a `DataFrame`.

        See Also
        --------
        Series.count: Number of non-NA elements in a Series.
        DataFrame.value_counts: Count unique combinations of columns.
        DataFrame.shape: Number of DataFrame rows and columns (including NA
            elements).
        DataFrame.isna: Boolean same-sized DataFrame showing places of NA
            elements.

        Examples
        --------
        Constructing DataFrame from a dictionary:

        >>> df = pd.DataFrame({"Person":
        ...                    ["John", "Myla", "Lewis", "John", "Myla"],
        ...                    "Age": [24., np.nan, 21., 33, 26],
        ...                    "Single": [False, True, True, True, False]})
        >>> df
           Person   Age  Single
        0    John  24.0   False
        1    Myla   NaN    True
        2   Lewis  21.0    True
        3    John  33.0    True
        4    Myla  26.0   False

        Notice the uncounted NA values:

        >>> df.count()
        Person    5
        Age       4
        Single    5
        dtype: int64

        Counts for each **row**:

        >>> df.count(axis='columns')
        0    3
        1    2
        2    3
        3    3
        4    3
        dtype: int64
        """
        axis = self._get_axis_number(axis)
        if level is not None:
            warnings.warn(
                "Using the level keyword in DataFrame and Series aggregations is "
                "deprecated and will be removed in a future version. Use groupby "
                "instead. df.count(level=1) should use df.groupby(level=1).count().",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
            res = self._count_level(level, axis=axis, numeric_only=numeric_only)
            return res.__finalize__(self, method="count")

        if numeric_only:
            frame = self._get_numeric_data()
        else:
            frame = self

        # GH #423
        if len(frame._get_axis(axis)) == 0:
            result = self._constructor_sliced(0, index=frame._get_agg_axis(axis))
        else:
            if frame._is_mixed_type or frame._mgr.any_extension_types:
                # the or any_extension_types is really only hit for single-
                # column frames with an extension array
                result = notna(frame).sum(axis=axis)
            else:
                # GH13407
                series_counts = notna(frame).sum(axis=axis)
                counts = series_counts.values
                result = self._constructor_sliced(
                    counts, index=frame._get_agg_axis(axis)
                )

        return result.astype("int64").__finalize__(self, method="count")
