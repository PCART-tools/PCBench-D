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
        aggregation_description="weighted window variance",
        agg_method="var",
    )
    def var(self, ddof: int = 1, numeric_only: bool = False, **kwargs):
        window_func = partial(window_aggregations.roll_weighted_var, ddof=ddof)
        kwargs.pop("name", None)
        return self._apply(window_func, name="var", numeric_only=numeric_only, **kwargs)
