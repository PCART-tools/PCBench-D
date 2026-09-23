    def render(
        self,
        *,
        buf: IO[str] | None,
        max_cols: int | None,
        verbose: bool | None,
        show_counts: bool | None,
    ) -> None:
        printer = DataFrameInfoPrinter(
            info=self,
            max_cols=max_cols,
            verbose=verbose,
            show_counts=show_counts,
        )
        printer.to_buffer(buf)
