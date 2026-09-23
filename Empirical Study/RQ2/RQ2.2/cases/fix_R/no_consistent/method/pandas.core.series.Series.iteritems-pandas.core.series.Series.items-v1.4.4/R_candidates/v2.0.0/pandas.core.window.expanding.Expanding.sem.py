    @doc(
        template_header,
        create_section_header("Parameters"),
        dedent(
            """
        ddof : int, default 1
            Delta Degrees of Freedom.  The divisor used in calculations
            is ``N - ddof``, where ``N`` represents the number of elements.\n
        """
        ).replace("\n", "", 1),
        kwargs_numeric_only,
        create_section_header("Returns"),
        template_returns,
        create_section_header("See Also"),
        template_see_also,
        create_section_header("Notes"),
        "A minimum of one period is required for the calculation.\n\n",
        create_section_header("Examples"),
        dedent(
            """
        >>> s = pd.Series([0, 1, 2, 3])

        >>> s.expanding().sem()
        0         NaN
        1    0.707107
        2    0.707107
        3    0.745356
        dtype: float64
        """
        ).replace("\n", "", 1),
        window_method="expanding",
        aggregation_description="standard error of mean",
        agg_method="sem",
    )
    def sem(self, ddof: int = 1, numeric_only: bool = False):
        return super().sem(ddof=ddof, numeric_only=numeric_only)
