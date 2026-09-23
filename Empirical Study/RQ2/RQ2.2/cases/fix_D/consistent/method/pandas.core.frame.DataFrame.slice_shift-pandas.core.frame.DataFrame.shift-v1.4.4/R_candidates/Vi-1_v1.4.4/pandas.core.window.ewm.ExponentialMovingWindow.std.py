    @doc(
        template_header,
        create_section_header("Parameters"),
        dedent(
            """
        bias : bool, default False
            Use a standard estimation bias correction.
        """
        ).replace("\n", "", 1),
        args_compat,
        kwargs_compat,
        create_section_header("Returns"),
        template_returns,
        create_section_header("See Also"),
        template_see_also[:-1],
        window_method="ewm",
        aggregation_description="(exponential weighted moment) standard deviation",
        agg_method="std",
    )
    def std(self, bias: bool = False, *args, **kwargs):
        nv.validate_window_func("std", args, kwargs)
        return zsqrt(self.var(bias=bias, **kwargs))
