    @doc(
        template_header,
        create_section_header("Parameters"),
        kwargs_numeric_only,
        args_compat,
        window_agg_numba_parameters(),
        kwargs_compat,
        create_section_header("Returns"),
        template_returns,
        create_section_header("See Also"),
        template_see_also,
        create_section_header("Notes"),
        numba_notes[:-1],
        window_method="expanding",
        aggregation_description="mean",
        agg_method="mean",
    )
    def mean(
        self,
        numeric_only: bool = False,
        *args,
        engine: str | None = None,
        engine_kwargs: dict[str, bool] | None = None,
        **kwargs,
    ):
        maybe_warn_args_and_kwargs(type(self), "mean", args, kwargs)
        nv.validate_expanding_func("mean", args, kwargs)
        return super().mean(
            numeric_only=numeric_only,
            engine=engine,
            engine_kwargs=engine_kwargs,
            **kwargs,
        )
