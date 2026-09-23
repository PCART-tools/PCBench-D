    @doc(
        template_header,
        create_section_header("Parameters"),
        kwargs_numeric_only,
        kwargs_scipy,
        create_section_header("Returns"),
        template_returns,
        create_section_header("See Also"),
        template_see_also,
        create_section_header("Examples"),
        dedent(
            """\
        >>> ser = pd.Series([0, 1, 5, 2, 8])

        To get an instance of :class:`~pandas.core.window.rolling.Window` we need
        to pass the parameter `win_type`.

        >>> type(ser.rolling(2, win_type='gaussian'))
        <class 'pandas.core.window.rolling.Window'>

        In order to use the `SciPy` Gaussian window we need to provide the parameters
        `M` and `std`. The parameter `M` corresponds to 2 in our example.
        We pass the second parameter `std` as a parameter of the following method
        (`sum` in this case):

        >>> ser.rolling(2, win_type='gaussian').sum(std=3)
        0         NaN
        1    0.986207
        2    5.917243
        3    6.903450
        4    9.862071
        dtype: float64
        """
        ),
        window_method="rolling",
        aggregation_description="weighted window sum",
        agg_method="sum",
    )
    def sum(self, numeric_only: bool = False, **kwargs):
        window_func = window_aggregations.roll_weighted_sum
        # error: Argument 1 to "_apply" of "Window" has incompatible type
        # "Callable[[ndarray, ndarray, int], ndarray]"; expected
        # "Callable[[ndarray, int, int], ndarray]"
        return self._apply(
            window_func,  # type: ignore[arg-type]
            name="sum",
            numeric_only=numeric_only,
            **kwargs,
        )
