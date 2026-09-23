    def agg(self, aggs: pli.Expr | Sequence[pli.Expr]) -> pli.DataFrame:
        return (
            self.df.lazy()
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
            .agg(aggs)
            .collect(no_optimization=True)
        )
