    @doc(
        template_header,
        create_section_header("Parameters"),
        kwargs_numeric_only,
        window_agg_numba_parameters(),
        create_section_header("Returns"),
        template_returns,
        create_section_header("See Also"),
        template_see_also,
        create_section_header("Notes"),
        numba_notes,
        create_section_header("Examples"),
        dedent(
            """\
        >>> ser = pd.Series([3, 2, 1, 4], index=['a', 'b', 'c', 'd'])
        >>> ser.expanding().max()
        a    3.0
        b    3.0
        c    3.0
        d    4.0
        dtype: float64
        """
        ),
        window_method="expanding",
        aggregation_description="maximum",
        agg_method="max",
    )
    def max(
        self,
        numeric_only: bool = False,
        engine: Literal["cython", "numba"] | None = None,
        engine_kwargs: dict[str, bool] | None = None,
    ):
        return super().max(
            numeric_only=numeric_only,
            engine=engine,
            engine_kwargs=engine_kwargs,
        )
