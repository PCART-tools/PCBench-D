    def __init__(
        self,
        df: DataFrame,
        index_column: IntoExpr,
        *,
        period: str | timedelta,
        offset: str | timedelta | None,
        closed: ClosedInterval,
        by: IntoExpr | Iterable[IntoExpr] | None,
        check_sorted: bool,
    ):
        period = _timedelta_to_pl_duration(period)
        offset = _timedelta_to_pl_duration(offset)

        self.df = df
        self.time_column = index_column
        self.period = period
        self.offset = offset
        self.closed = closed
        self.by = by
        self.check_sorted = check_sorted
