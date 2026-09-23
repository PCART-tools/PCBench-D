    @doc(
        template_header,
        create_section_header("Parameters"),
        dedent(
            """\
        bias : bool, default False
            Use a standard estimation bias correction.
        """
        ),
        kwargs_numeric_only,
        create_section_header("Returns"),
        template_returns,
        create_section_header("See Also"),
        template_see_also,
        create_section_header("Examples"),
        dedent(
            """\
        >>> ser = pd.Series([1, 2, 3, 4])
        >>> ser.ewm(alpha=.2).var()
        0         NaN
        1    0.500000
        2    0.991803
        3    1.631547
        dtype: float64
        """
        ),
        window_method="ewm",
        aggregation_description="(exponential weighted moment) variance",
        agg_method="var",
    )
    def var(self, bias: bool = False, numeric_only: bool = False):
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

        return self._apply(var_func, name="var", numeric_only=numeric_only)
