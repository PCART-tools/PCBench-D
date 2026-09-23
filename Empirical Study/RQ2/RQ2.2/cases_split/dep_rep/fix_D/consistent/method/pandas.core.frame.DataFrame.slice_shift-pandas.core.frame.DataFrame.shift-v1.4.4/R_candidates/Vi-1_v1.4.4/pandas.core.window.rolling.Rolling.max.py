    @doc(
        template_header,
        create_section_header("Parameters"),
        args_compat,
        window_agg_numba_parameters(),
        kwargs_compat,
        create_section_header("Returns"),
        template_returns,
        create_section_header("See Also"),
        template_see_also,
        create_section_header("Notes"),
        numba_notes[:-1],
        window_method="rolling",
        aggregation_description="maximum",
        agg_method="max",
    )
    def max(
        self,
        *args,
        engine: str | None = None,
        engine_kwargs: dict[str, bool] | None = None,
        **kwargs,
    ):
        nv.validate_rolling_func("max", args, kwargs)
        return super().max(*args, engine=engine, engine_kwargs=engine_kwargs, **kwargs)
