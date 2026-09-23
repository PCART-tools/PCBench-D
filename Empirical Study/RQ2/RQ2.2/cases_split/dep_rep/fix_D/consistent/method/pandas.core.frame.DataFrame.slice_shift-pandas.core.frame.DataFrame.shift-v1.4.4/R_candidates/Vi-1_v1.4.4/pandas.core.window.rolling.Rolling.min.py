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
        numba_notes,
        create_section_header("Examples"),
        dedent(
            """
        Performing a rolling minimum with a window size of 3.

        >>> s = pd.Series([4, 3, 5, 2, 6])
        >>> s.rolling(3).min()
        0    NaN
        1    NaN
        2    3.0
        3    2.0
        4    2.0
        dtype: float64
        """
        ).replace("\n", "", 1),
        window_method="rolling",
        aggregation_description="minimum",
        agg_method="min",
    )
    def min(
        self,
        *args,
        engine: str | None = None,
        engine_kwargs: dict[str, bool] | None = None,
        **kwargs,
    ):
        nv.validate_rolling_func("min", args, kwargs)
        return super().min(*args, engine=engine, engine_kwargs=engine_kwargs, **kwargs)
