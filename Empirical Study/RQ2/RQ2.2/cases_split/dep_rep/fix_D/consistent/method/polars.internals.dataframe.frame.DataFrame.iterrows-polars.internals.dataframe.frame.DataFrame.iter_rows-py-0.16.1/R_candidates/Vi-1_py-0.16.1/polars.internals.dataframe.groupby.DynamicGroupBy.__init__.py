    def __init__(
        self,
        df: DF,
        index_column: str,
        every: str | timedelta,
        period: str | timedelta | None,
        offset: str | timedelta | None,
        truncate: bool,
        include_boundaries: bool,
        closed: ClosedInterval,
        by: str | pli.Expr | Sequence[str | pli.Expr] | None,
        start_by: StartBy,
    ):
        period = _timedelta_to_pl_duration(period)
        offset = _timedelta_to_pl_duration(offset)
        every = _timedelta_to_pl_duration(every)

        self.df = df
        self.time_column = index_column
        self.every = every
        self.period = period
        self.offset = offset
        self.truncate = truncate
        self.include_boundaries = include_boundaries
        self.closed = closed
        self.by = by
        self.start_by = start_by
