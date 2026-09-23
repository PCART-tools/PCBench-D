    def __iter__(self) -> DynamicGroupBy[DF]:
        temp_col = "__POLARS_GB_GROUP_INDICES"
        groups_df = (
            self.df.lazy()
            .with_row_count(name=temp_col)
            .groupby_dynamic(
                index_column=self.time_column,
                every=self.every,
                period=self.period,
                offset=self.offset,
                truncate=self.truncate,
                include_boundaries=self.include_boundaries,
                closed=self.closed,
                by=self.by,
                start_by=self.start_by,
            )
            .agg(pli.col(temp_col))
            .collect(no_optimization=True)
        )

        group_names = groups_df.select(pli.all().exclude(temp_col))

        # When grouping by a single column, group name is a single value
        # When grouping by multiple columns, group name is a tuple of values
        self._group_names: Iterator[object] | Iterator[tuple[object, ...]]
        if self.by is None:
            self._group_names = iter(group_names.to_series())
        else:
            self._group_names = group_names.iter_rows()

        self._group_indices = groups_df.select(temp_col).to_series()
        self._current_index = 0

        return self
