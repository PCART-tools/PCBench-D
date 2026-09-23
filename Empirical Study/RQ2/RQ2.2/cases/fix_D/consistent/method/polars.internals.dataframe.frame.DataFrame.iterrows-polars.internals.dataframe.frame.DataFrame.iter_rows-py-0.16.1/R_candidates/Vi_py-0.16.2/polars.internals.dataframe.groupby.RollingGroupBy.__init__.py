    def __init__(
        self,
        df: DF,
        index_column: str,
        period: str | timedelta,
        offset: str | timedelta | None,
        closed: ClosedInterval,
        by: str | pli.Expr | Sequence[str | pli.Expr] | None,
    ):
        period = _timedelta_to_pl_duration(period)
        offset = _timedelta_to_pl_duration(offset)

        self.df = df
        self.time_column = index_column
        self.period = period
        self.offset = offset
        self.closed = closed
        self.by = by
