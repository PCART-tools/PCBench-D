    def __init__(
        self,
        df: DataFrame,
        index_column: IntoExpr,
        *,
        every: str | timedelta,
        period: str | timedelta | None,
        offset: str | timedelta | None,
        truncate: bool | None,
        include_boundaries: bool,
        closed: ClosedInterval,
        label: Label,
        by: IntoExpr | Iterable[IntoExpr] | None,
        start_by: StartBy,
        check_sorted: bool,
    ):
        every = _timedelta_to_pl_duration(every)
        period = _timedelta_to_pl_duration(period)
        offset = _timedelta_to_pl_duration(offset)

        self.df = df
        self.time_column = index_column
        self.every = every
        self.period = period
        self.offset = offset
        self.truncate = truncate
        self.label = label
        self.include_boundaries = include_boundaries
        self.closed = closed
        self.by = by
        self.start_by = start_by
        self.check_sorted = check_sorted
