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
            .rolling(
                index_column=self.time_column,
                period=self.period,
                offset=self.offset,
                closed=self.closed,
                by=self.by,
                check_sorted=self.check_sorted,
            )
            .agg(*aggs, **named_aggs)
            .collect(no_optimization=True)
        )
