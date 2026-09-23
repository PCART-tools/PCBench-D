    def __init__(
        self,
        df: DataFrame,
        index_column: IntoExpr,
        *,
        every: str | timedelta,
        period: str | timedelta | None,
        offset: str | timedelta | None,
        include_boundaries: bool,
        closed: ClosedInterval,
        label: Label,
        group_by: IntoExpr | Iterable[IntoExpr] | None,
        start_by: StartBy,
    ):
        every = parse_as_duration_string(every)
        period = parse_as_duration_string(period)
        offset = parse_as_duration_string(offset)

        self.df = df
        self.time_column = index_column
        self.every = every
        self.period = period
        self.offset = offset
        self.label = label
        self.include_boundaries = include_boundaries
        self.closed = closed
        self.group_by = group_by
        self.start_by = start_by
