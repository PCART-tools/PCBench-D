    def agg(
        self,
        *aggs: IntoExpr | Iterable[IntoExpr],
        **named_aggs: IntoExpr,
    ) -> DataFrame:
        """
        Compute aggregations for each group of a group by operation.

        Parameters
        ----------
        *aggs
            Aggregations to compute for each group of the group by operation,
            specified as positional arguments.
            Accepts expression input. Strings are parsed as column names.
        **named_aggs
            Additional aggregations, specified as keyword arguments.
            The resulting columns will be renamed to the keyword used.
        """
        return (
            self.df.lazy()
            .group_by_dynamic(
                index_column=self.time_column,
                every=self.every,
                period=self.period,
                offset=self.offset,
                label=self.label,
                include_boundaries=self.include_boundaries,
                closed=self.closed,
                group_by=self.group_by,
                start_by=self.start_by,
            )
            .agg(*aggs, **named_aggs)
            .collect(no_optimization=True)
        )
