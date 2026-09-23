    def __iter__(self) -> Self:
        temp_col = "__POLARS_GB_GROUP_INDICES"
        groups_df = (
            self.df.lazy()
            .rolling(
                index_column=self.time_column,
                period=self.period,
                offset=self.offset,
                closed=self.closed,
                group_by=self.group_by,
            )
            .agg(F.first().agg_groups().alias(temp_col))
            .collect(no_optimization=True)
        )

        self._group_names = groups_df.select(F.all().exclude(temp_col)).iter_rows()
        self._group_indices = groups_df.select(temp_col).to_series()
        self._current_index = 0

        return self
