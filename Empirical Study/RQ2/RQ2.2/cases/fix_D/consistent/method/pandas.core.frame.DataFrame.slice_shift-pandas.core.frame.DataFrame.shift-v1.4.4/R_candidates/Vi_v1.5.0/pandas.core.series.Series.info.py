    @doc(INFO_DOCSTRING, **series_sub_kwargs)
    def info(
        self,
        verbose: bool | None = None,
        buf: IO[str] | None = None,
        max_cols: int | None = None,
        memory_usage: bool | str | None = None,
        show_counts: bool = True,
    ) -> None:
        return SeriesInfo(self, memory_usage).render(
            buf=buf,
            max_cols=max_cols,
            verbose=verbose,
            show_counts=show_counts,
        )
