    @final
    def _value_counts(
        self,
        subset: Sequence[Hashable] | None = None,
        normalize: bool = False,
        sort: bool = True,
        ascending: bool = False,
        dropna: bool = True,
    ) -> DataFrame | Series:
        """
        Shared implementation of value_counts for SeriesGroupBy and DataFrameGroupBy.

        SeriesGroupBy additionally supports a bins argument. See the docstring of
        DataFrameGroupBy.value_counts for a description of arguments.
        """
        if self.axis == 1:
            raise NotImplementedError(
                "DataFrameGroupBy.value_counts only handles axis=0"
            )
        name = "proportion" if normalize else "count"

        df = self.obj
        obj = self._obj_with_exclusions

        in_axis_names = {
            grouping.name for grouping in self.grouper.groupings if grouping.in_axis
        }
        if isinstance(obj, Series):
            _name = obj.name
            keys = [] if _name in in_axis_names else [obj]
        else:
            unique_cols = set(obj.columns)
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
                obj.iloc[:, idx]
                for idx, _name in enumerate(obj.columns)
                if _name not in in_axis_names and _name in subsetted
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
        result_series.name = name

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
            result_series = result_series.sort_values(ascending=ascending).sort_index(
                level=index_level, sort_remaining=False
            )

        result: Series | DataFrame
        if self.as_index:
            result = result_series
        else:
            # Convert to frame
            index = result_series.index
            columns = com.fill_missing_names(index.names)
            if name in columns:
                raise ValueError(f"Column label '{name}' is duplicate of result column")
            result_series.name = name
            result_series.index = index.set_names(range(len(columns)))
            result_frame = result_series.reset_index()
            result_frame.columns = columns + [name]
            result = result_frame
        return result.__finalize__(self.obj, method="value_counts")
