    def agg(self, aggs: pli.Expr | Sequence[pli.Expr]) -> pli.DataFrame:
        return (
            self.df.lazy()
            .groupby_rolling(
                index_column=self.time_column,
                period=self.period,
                offset=self.offset,
                closed=self.closed,
                by=self.by,
            )
            .agg(aggs)
            .collect(no_optimization=True)
        )
