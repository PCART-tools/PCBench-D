    @doc(
        template_header,
        ".. versionadded:: 1.4.0 \n\n",
        create_section_header("Parameters"),
        dedent(
            """
        method : {{'average', 'min', 'max'}}, default 'average'
            How to rank the group of records that have the same value (i.e. ties):

            * average: average rank of the group
            * min: lowest rank in the group
            * max: highest rank in the group

        ascending : bool, default True
            Whether or not the elements should be ranked in ascending order.
        pct : bool, default False
            Whether or not to display the returned rankings in percentile
            form.
        """
        ).replace("\n", "", 1),
        kwargs_numeric_only,
        create_section_header("Returns"),
        template_returns,
        create_section_header("See Also"),
        template_see_also,
        create_section_header("Examples"),
        dedent(
            """
        >>> s = pd.Series([1, 4, 2, 3, 5, 3])
        >>> s.expanding().rank()
        0    1.0
        1    2.0
        2    2.0
        3    3.0
        4    5.0
        5    3.5
        dtype: float64

        >>> s.expanding().rank(method="max")
        0    1.0
        1    2.0
        2    2.0
        3    3.0
        4    5.0
        5    4.0
        dtype: float64

        >>> s.expanding().rank(method="min")
        0    1.0
        1    2.0
        2    2.0
        3    3.0
        4    5.0
        5    3.0
        dtype: float64
        """
        ).replace("\n", "", 1),
        window_method="expanding",
        aggregation_description="rank",
        agg_method="rank",
    )
    def rank(
        self,
        method: WindowingRankType = "average",
        ascending: bool = True,
        pct: bool = False,
        numeric_only: bool = False,
    ):
        return super().rank(
            method=method,
            ascending=ascending,
            pct=pct,
            numeric_only=numeric_only,
        )
