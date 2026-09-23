    def value_counts(
        self,
        subset: Sequence[Hashable] | None = None,
        normalize: bool = False,
        sort: bool = True,
        ascending: bool = False,
        dropna: bool = True,
    ) -> Series:
        """
        Return a Series containing counts of unique rows in the DataFrame.

        .. versionadded:: 1.1.0

        Parameters
        ----------
        subset : label or list of labels, optional
            Columns to use when counting unique combinations.
        normalize : bool, default False
            Return proportions rather than frequencies.
        sort : bool, default True
            Sort by frequencies.
        ascending : bool, default False
            Sort in ascending order.
        dropna : bool, default True
            Don’t include counts of rows that contain NA values.

            .. versionadded:: 1.3.0

        Returns
        -------
        Series

        See Also
        --------
        Series.value_counts: Equivalent method on Series.

        Notes
        -----
        The returned Series will have a MultiIndex with one level per input
        column but an Index (non-multi) for a single label. By default, rows
        that contain any NA values are omitted from the result. By default,
        the resulting Series will be in descending order so that the first
        element is the most frequently-occurring row.

        Examples
        --------
        >>> df = pd.DataFrame({'num_legs': [2, 4, 4, 6],
        ...                    'num_wings': [2, 0, 0, 0]},
        ...                   index=['falcon', 'dog', 'cat', 'ant'])
        >>> df
                num_legs  num_wings
        falcon         2          2
        dog            4          0
        cat            4          0
        ant            6          0

        >>> df.value_counts()
        num_legs  num_wings
        4         0            2
        2         2            1
        6         0            1
        Name: count, dtype: int64

        >>> df.value_counts(sort=False)
        num_legs  num_wings
        2         2            1
        4         0            2
        6         0            1
        Name: count, dtype: int64

        >>> df.value_counts(ascending=True)
        num_legs  num_wings
        2         2            1
        6         0            1
        4         0            2
        Name: count, dtype: int64

        >>> df.value_counts(normalize=True)
        num_legs  num_wings
        4         0            0.50
        2         2            0.25
        6         0            0.25
        Name: proportion, dtype: float64

        With `dropna` set to `False` we can also count rows with NA values.

        >>> df = pd.DataFrame({'first_name': ['John', 'Anne', 'John', 'Beth'],
        ...                    'middle_name': ['Smith', pd.NA, pd.NA, 'Louise']})
        >>> df
          first_name middle_name
        0       John       Smith
        1       Anne        <NA>
        2       John        <NA>
        3       Beth      Louise

        >>> df.value_counts()
        first_name  middle_name
        Beth        Louise         1
        John        Smith          1
        Name: count, dtype: int64

        >>> df.value_counts(dropna=False)
        first_name  middle_name
        Anne        NaN            1
        Beth        Louise         1
        John        Smith          1
                    NaN            1
        Name: count, dtype: int64

        >>> df.value_counts("first_name")
        first_name
        John    2
        Anne    1
        Beth    1
        Name: count, dtype: int64
        """
        if subset is None:
            subset = self.columns.tolist()

        name = "proportion" if normalize else "count"
        counts = self.groupby(subset, dropna=dropna).grouper.size()
        counts.name = name

        if sort:
            counts = counts.sort_values(ascending=ascending)
        if normalize:
            counts /= counts.sum()

        # Force MultiIndex for single column
        if is_list_like(subset) and len(subset) == 1:
            counts.index = MultiIndex.from_arrays(
                [counts.index], names=[counts.index.name]
            )

        return counts
