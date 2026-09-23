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
        "A minimum of three periods is required for the rolling calculation.\n",
        window_method="rolling",
        aggregation_description="unbiased skewness",
        agg_method="skew",
    )
    def skew(self, numeric_only: bool = False):
        return super().skew(numeric_only=numeric_only)
