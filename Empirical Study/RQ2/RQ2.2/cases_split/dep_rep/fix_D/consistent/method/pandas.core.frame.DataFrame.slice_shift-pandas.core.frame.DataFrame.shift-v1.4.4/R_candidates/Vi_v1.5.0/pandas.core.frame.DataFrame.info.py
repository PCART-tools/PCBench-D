    @doc(INFO_DOCSTRING, **frame_sub_kwargs)
    def info(
        self,
        verbose: bool | None = None,
        buf: WriteBuffer[str] | None = None,
        max_cols: int | None = None,
        memory_usage: bool | str | None = None,
        show_counts: bool | None = None,
        null_counts: bool | None = None,
    ) -> None:
        if null_counts is not None:
            if show_counts is not None:
                raise ValueError("null_counts used with show_counts. Use show_counts.")
            warnings.warn(
                "null_counts is deprecated. Use show_counts instead",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
            show_counts = null_counts
        info = DataFrameInfo(
            data=self,
            memory_usage=memory_usage,
        )
        info.render(
            buf=buf,
            max_cols=max_cols,
            verbose=verbose,
            show_counts=show_counts,
        )
