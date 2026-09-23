    @doc(
        template_header,
        ".. versionadded:: 1.0.0 \n\n",
        create_section_header("Parameters"),
        kwargs_numeric_only,
        kwargs_scipy,
        create_section_header("Returns"),
        template_returns,
        create_section_header("See Also"),
        template_see_also[:-1],
        window_method="rolling",
        aggregation_description="weighted window standard deviation",
        agg_method="std",
    )
    def std(self, ddof: int = 1, numeric_only: bool = False, *args, **kwargs):
        nv.validate_window_func("std", args, kwargs)
        return zsqrt(
            self.var(ddof=ddof, name="std", numeric_only=numeric_only, **kwargs)
        )
