    @doc(
        template_header,
        create_section_header("Returns"),
        template_returns,
        create_section_header("See Also"),
        template_see_also,
        create_section_header("Examples"),
        dedent(
            """\
        >>> ser = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
        >>> ser.expanding().count()
        a    1.0
        b    2.0
        c    3.0
        d    4.0
        dtype: float64
        """
        ),
        window_method="expanding",
        aggregation_description="count of non NaN observations",
        agg_method="count",
    )
    def count(self, numeric_only: bool = False):
        return super().count(numeric_only=numeric_only)
