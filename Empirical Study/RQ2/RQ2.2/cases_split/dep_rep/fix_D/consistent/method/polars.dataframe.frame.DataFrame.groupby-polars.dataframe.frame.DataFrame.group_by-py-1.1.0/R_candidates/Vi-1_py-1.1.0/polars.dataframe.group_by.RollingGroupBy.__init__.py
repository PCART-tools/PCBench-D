    def __init__(
        self,
        df: DataFrame,
        index_column: IntoExpr,
        *,
        period: str | timedelta,
        offset: str | timedelta | None,
        closed: ClosedInterval,
        group_by: IntoExpr | Iterable[IntoExpr] | None,
    ):
        period = parse_as_duration_string(period)
        offset = parse_as_duration_string(offset)

        self.df = df
        self.time_column = index_column
        self.period = period
        self.offset = offset
        self.closed = closed
        self.group_by = group_by
