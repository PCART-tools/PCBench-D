    def __init__(
        self,
        info: DataFrameInfo,
        max_cols: int | None = None,
        verbose: bool | None = None,
        show_counts: bool | None = None,
    ) -> None:
        self.info = info
        self.data = info.data
        self.verbose = verbose
        self.max_cols = self._initialize_max_cols(max_cols)
        self.show_counts = self._initialize_show_counts(show_counts)
