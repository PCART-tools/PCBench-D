    def value_counts(
        self,
        subset: Sequence[Hashable] | None = None,
        normalize: bool = False,
        sort: bool = True,
        ascending: bool = False,
        dropna: bool = True,
    ) -> DataFrame | Series:
        """
        Return a Series or DataFrame containing counts of unique rows.

        .. versionadded:: 1.4.0

        Parameters
        ----------
        subset : list-like, optional
            Columns to use when counting unique combinations.
        normalize : bool, default False
            Return proportions rather than frequencies.
        sort : bool, default True
            Sort by frequencies.
        ascending : bool, default False
            Sort in ascending order.
        dropna : bool, default True
            Don’t include counts of rows that contain NA values.

        Returns
        -------
        Series or DataFrame
            Series if the groupby as_index is True, otherwise DataFrame.

        See Also
        --------
        Series.value_counts: Equivalent method on Series.
        DataFrame.value_counts: Equivalent method on DataFrame.
        SeriesGroupBy.value_counts: Equivalent method on SeriesGroupBy.

        Notes
        -----
        - If the groupby as_index is True then the returned Series will have a
          MultiIndex with one level per input column.
        - If the groupby as_index is False then the returned DataFrame will have an
          additional column with the value_counts. The column is labelled 'count' or
          'proportion', depending on the ``normalize`` parameter.

        By default, rows that contain any NA values are omitted from
        the result.

        By default, the result will be in descending order so that the
        first element of each group is the most frequently-occurring row.

        Examples
        --------
        >>> df = pd.DataFrame({
        ...    'gender': ['male', 'male', 'female', 'male', 'female', 'male'],
        ...    'education': ['low', 'medium', 'high', 'low', 'high', 'low'],
        ...    'country': ['US', 'FR', 'US', 'FR', 'FR', 'FR']
        ... })

        >>> df
                gender  education   country
        0       male    low         US
        1       male    medium      FR
        2       female  high        US
        3       male    low         FR
        4       female  high        FR
        5       male    low         FR

        >>> df.groupby('gender').value_counts()
        gender  education  country
        female  high       FR         1
                           US         1
        male    low        FR         2
                           US         1
                medium     FR         1
        dtype: int64

        >>> df.groupby('gender').value_counts(ascending=True)
        gender  education  country
        female  high       FR         1
                           US         1
        male    low        US         1
                medium     FR         1
                low        FR         2
        dtype: int64

        >>> df.groupby('gender').value_counts(normalize=True)
        gender  education  country
        female  high       FR         0.50
                           US         0.50
        male    low        FR         0.50
                           US         0.25
                medium     FR         0.25
        dtype: float64

        >>> df.groupby('gender', as_index=False).value_counts()
           gender education country  count
        0  female      high      FR      1
        1  female      high      US      1
        2    male       low      FR      2
        3    male       low      US      1
        4    male    medium      FR      1

        >>> df.groupby('gender', as_index=False).value_counts(normalize=True)
           gender education country  proportion
        0  female      high      FR        0.50
        1  female      high      US        0.50
        2    male       low      FR        0.50
        3    male       low      US        0.25
        4    male    medium      FR        0.25
        """
        if self.axis == 1:
            raise NotImplementedError(
                "DataFrameGroupBy.value_counts only handles axis=0"
            )

        with self._group_selection_context():
            df = self.obj

            in_axis_names = {
                grouping.name for grouping in self.grouper.groupings if grouping.in_axis
            }
            if isinstance(self._selected_obj, Series):
                name = self._selected_obj.name
                keys = [] if name in in_axis_names else [self._selected_obj]
            else:
                unique_cols = set(self._selected_obj.columns)
                if subset is not None:
                    subsetted = set(subset)
                    clashing = subsetted & set(in_axis_names)
                    if clashing:
                        raise ValueError(
                            f"Keys {clashing} in subset cannot be in "
                            "the groupby column keys."
                        )
                    doesnt_exist = subsetted - unique_cols
                    if doesnt_exist:
                        raise ValueError(
                            f"Keys {doesnt_exist} in subset do not "
                            f"exist in the DataFrame."
                        )
                else:
                    subsetted = unique_cols

                keys = [
                    # Can't use .values because the column label needs to be preserved
                    self._selected_obj.iloc[:, idx]
                    for idx, name in enumerate(self._selected_obj.columns)
                    if name not in in_axis_names and name in subsetted
                ]

            groupings = list(self.grouper.groupings)
            for key in keys:
                grouper, _, _ = get_grouper(
                    df,
                    key=key,
                    axis=self.axis,
                    sort=self.sort,
                    observed=False,
                    dropna=dropna,
                )
                groupings += list(grouper.groupings)

            # Take the size of the overall columns
            gb = df.groupby(
                groupings,
                sort=self.sort,
                observed=self.observed,
                dropna=self.dropna,
            )
            result_series = cast(Series, gb.size())

            # GH-46357 Include non-observed categories
            # of non-grouping columns regardless of `observed`
            if any(
                isinstance(grouping.grouping_vector, (Categorical, CategoricalIndex))
                and not grouping._observed
                for grouping in groupings
            ):
                levels_list = [ping.result_index for ping in groupings]
                multi_index, _ = MultiIndex.from_product(
                    levels_list, names=[ping.name for ping in groupings]
                ).sortlevel()
                result_series = result_series.reindex(multi_index, fill_value=0)

            if normalize:
                # Normalize the results by dividing by the original group sizes.
                # We are guaranteed to have the first N levels be the
                # user-requested grouping.
                levels = list(
                    range(len(self.grouper.groupings), result_series.index.nlevels)
                )
                indexed_group_size = result_series.groupby(
                    result_series.index.droplevel(levels),
                    sort=self.sort,
                    dropna=self.dropna,
                ).transform("sum")
                result_series /= indexed_group_size

                # Handle groups of non-observed categories
                result_series = result_series.fillna(0.0)

            if sort:
                # Sort the values and then resort by the main grouping
                index_level = range(len(self.grouper.groupings))
                result_series = result_series.sort_values(
                    ascending=ascending
                ).sort_index(level=index_level, sort_remaining=False)

            result: Series | DataFrame
            if self.as_index:
                result = result_series
            else:
                # Convert to frame
                name = "proportion" if normalize else "count"
                index = result_series.index
                columns = com.fill_missing_names(index.names)
                if name in columns:
                    raise ValueError(
                        f"Column label '{name}' is duplicate of result column"
                    )
                result_series.name = name
                result_series.index = index.set_names(range(len(columns)))
                result_frame = result_series.reset_index()
                result_frame.columns = columns + [name]
                result = result_frame
            return result.__finalize__(self.obj, method="value_counts")
