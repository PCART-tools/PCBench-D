    @doc(
        template_header,
        create_section_header("Parameters"),
        kwargs_numeric_only,
        create_section_header("Returns"),
        template_returns,
        create_section_header("See Also"),
        template_see_also,
        create_section_header("Examples"),
        dedent(
            """
        >>> s = pd.Series([2, 3, np.nan, 10])
        >>> s.rolling(2).count()
        0    1.0
        1    2.0
        2    1.0
        3    1.0
        dtype: float64
        >>> s.rolling(3).count()
        0    1.0
        1    2.0
        2    2.0
        3    2.0
        dtype: float64
        >>> s.rolling(4).count()
        0    1.0
        1    2.0
        2    2.0
        3    3.0
        dtype: float64
        """
        ).replace("\n", "", 1),
        window_method="rolling",
        aggregation_description="count of non NaN observations",
        agg_method="count",
    )
    def count(self, numeric_only: bool = False):
        if self.min_periods is None:
            warnings.warn(
                (
                    "min_periods=None will default to the size of window "
                    "consistent with other methods in a future version. "
                    "Specify min_periods=0 instead."
                ),
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
            self.min_periods = 0
            result = super().count()
            self.min_periods = None
        else:
            result = super().count(numeric_only)
        return result
