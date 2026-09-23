    def render(
        self,
        *,
        buf: WriteBuffer[str] | None = None,
        max_cols: int | None = None,
        verbose: bool | None = None,
        show_counts: bool | None = None,
    ) -> None:
        if max_cols is not None:
            raise ValueError(
                "Argument `max_cols` can only be passed "
                "in DataFrame.info, not Series.info"
            )
        printer = SeriesInfoPrinter(
            info=self,
            verbose=verbose,
            show_counts=show_counts,
        )
        printer.to_buffer(buf)
