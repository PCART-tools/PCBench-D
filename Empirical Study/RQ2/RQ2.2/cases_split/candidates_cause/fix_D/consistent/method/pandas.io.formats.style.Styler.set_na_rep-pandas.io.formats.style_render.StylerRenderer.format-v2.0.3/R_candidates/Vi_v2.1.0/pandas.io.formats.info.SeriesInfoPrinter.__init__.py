    def __init__(
        self,
        info: SeriesInfo,
        verbose: bool | None = None,
        show_counts: bool | None = None,
    ) -> None:
        self.info = info
        self.data = info.data
        self.verbose = verbose
        self.show_counts = self._initialize_show_counts(show_counts)
