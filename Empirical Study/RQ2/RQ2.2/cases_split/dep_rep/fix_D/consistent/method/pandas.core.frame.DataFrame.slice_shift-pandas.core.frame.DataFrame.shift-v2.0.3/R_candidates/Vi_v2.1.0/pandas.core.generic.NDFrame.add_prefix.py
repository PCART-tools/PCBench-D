    @final
    def add_prefix(self, prefix: str, axis: Axis | None = None) -> Self:
        """
        Prefix labels with string `prefix`.

        For Series, the row labels are prefixed.
        For DataFrame, the column labels are prefixed.

        Parameters
        ----------
        prefix : str
            The string to add before each label.
        axis : {0 or 'index', 1 or 'columns', None}, default None
            Axis to add prefix on

            .. versionadded:: 2.0.0

        Returns
        -------
        Series or DataFrame
            New Series or DataFrame with updated labels.

        See Also
        --------
        Series.add_suffix: Suffix row labels with string `suffix`.
        DataFrame.add_suffix: Suffix column labels with string `suffix`.

        Examples
        --------
        >>> s = pd.Series([1, 2, 3, 4])
        >>> s
        0    1
        1    2
        2    3
        3    4
        dtype: int64

        >>> s.add_prefix('item_')
        item_0    1
        item_1    2
        item_2    3
        item_3    4
        dtype: int64

        >>> df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [3, 4, 5, 6]})
        >>> df
           A  B
        0  1  3
        1  2  4
        2  3  5
        3  4  6

        >>> df.add_prefix('col_')
             col_A  col_B
        0       1       3
        1       2       4
        2       3       5
        3       4       6
        """
        f = lambda x: f"{prefix}{x}"

        axis_name = self._info_axis_name
        if axis is not None:
            axis_name = self._get_axis_name(axis)

        mapper = {axis_name: f}

        # error: Incompatible return value type (got "Optional[Self]",
        # expected "Self")
        # error: Argument 1 to "rename" of "NDFrame" has incompatible type
        # "**Dict[str, partial[str]]"; expected "Union[str, int, None]"
        # error: Keywords must be strings
        return self._rename(**mapper)  # type: ignore[return-value, arg-type, misc]
