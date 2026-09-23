    @doc(
        template_header,
        create_section_header("Parameters"),
        kwargs_numeric_only,
        create_section_header("Returns"),
        template_returns,
        create_section_header("See Also"),
        "scipy.stats.skew : Third moment of a probability density.\n",
        template_see_also,
        create_section_header("Notes"),
        dedent(
            """
        A minimum of three periods is required for the rolling calculation.\n
        """
        ),
        create_section_header("Examples"),
        dedent(
            """\
        >>> ser = pd.Series([1, 5, 2, 7, 12, 6])
        >>> ser.rolling(3).skew().round(6)
        0         NaN
        1         NaN
        2    1.293343
        3   -0.585583
        4    0.000000
        5    1.545393
        dtype: float64
        """
        ),
        window_method="rolling",
        aggregation_description="unbiased skewness",
        agg_method="skew",
    )
    def skew(self, numeric_only: bool = False):
        return super().skew(numeric_only=numeric_only)
