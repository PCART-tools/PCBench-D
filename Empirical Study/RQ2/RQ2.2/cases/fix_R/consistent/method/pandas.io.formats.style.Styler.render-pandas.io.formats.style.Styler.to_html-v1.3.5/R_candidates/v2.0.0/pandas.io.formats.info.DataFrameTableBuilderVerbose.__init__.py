    def __init__(
        self,
        *,
        info: DataFrameInfo,
        with_counts: bool,
    ) -> None:
        self.info = info
        self.with_counts = with_counts
        self.strrows: Sequence[Sequence[str]] = list(self._gen_rows())
        self.gross_column_widths: Sequence[int] = self._get_gross_column_widths()
