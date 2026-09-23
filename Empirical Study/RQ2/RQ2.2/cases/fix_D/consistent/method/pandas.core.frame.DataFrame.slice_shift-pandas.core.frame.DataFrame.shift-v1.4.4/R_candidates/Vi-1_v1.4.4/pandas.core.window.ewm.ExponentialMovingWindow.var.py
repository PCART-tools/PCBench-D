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
        aggregation_description="(exponential weighted moment) variance",
        agg_method="var",
    )
    def var(self, bias: bool = False, *args, **kwargs):
        nv.validate_window_func("var", args, kwargs)
        window_func = window_aggregations.ewmcov
        wfunc = partial(
            window_func,
            com=self._com,
            adjust=self.adjust,
            ignore_na=self.ignore_na,
            bias=bias,
        )

        def var_func(values, begin, end, min_periods):
            return wfunc(values, begin, end, min_periods, values)

        return self._apply(var_func)
