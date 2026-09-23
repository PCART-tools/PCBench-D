    def __init__(
        self,
        df: DataFrame,
        *,
        max_cols: int = 75,
        max_rows: int = 40,
        from_series: bool = False,
    ):
        self.df = df
        self.elements: list[str] = []
        self.max_cols = max_cols
        self.max_rows = max_rows
        self.from_series = from_series
        self.row_idx: Iterable[int]
        self.col_idx: Iterable[int]

        if max_rows < df.height:
            half, rest = divmod(max_rows, 2)
            self.row_idx = [
                *list(range(half + rest)),
                -1,
                *list(range(df.height - half, df.height)),
            ]
        else:
            self.row_idx = range(df.height)
        if max_cols < df.width:
            self.col_idx = [
                *list(range(max_cols // 2)),
                -1,
                *list(range(df.width - max_cols // 2, df.width)),
            ]
        else:
            self.col_idx = range(df.width)
