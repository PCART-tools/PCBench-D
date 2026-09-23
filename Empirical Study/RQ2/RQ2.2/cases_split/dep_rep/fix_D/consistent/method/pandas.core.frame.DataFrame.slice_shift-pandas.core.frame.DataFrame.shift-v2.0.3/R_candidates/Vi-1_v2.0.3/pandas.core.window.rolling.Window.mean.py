    @doc(
        template_header,
        create_section_header("Parameters"),
        kwargs_numeric_only,
        kwargs_scipy,
        create_section_header("Returns"),
        template_returns,
        create_section_header("See Also"),
        template_see_also[:-1],
        window_method="rolling",
        aggregation_description="weighted window mean",
        agg_method="mean",
    )
    def mean(self, numeric_only: bool = False, **kwargs):
        window_func = window_aggregations.roll_weighted_mean
        # error: Argument 1 to "_apply" of "Window" has incompatible type
        # "Callable[[ndarray, ndarray, int], ndarray]"; expected
        # "Callable[[ndarray, int, int], ndarray]"
        return self._apply(
            window_func,  # type: ignore[arg-type]
            name="mean",
            numeric_only=numeric_only,
            **kwargs,
        )
