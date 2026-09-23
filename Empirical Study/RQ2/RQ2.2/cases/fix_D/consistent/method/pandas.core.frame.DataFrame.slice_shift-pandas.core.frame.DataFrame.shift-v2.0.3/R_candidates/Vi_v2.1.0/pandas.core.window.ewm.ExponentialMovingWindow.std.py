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
        >>> ser.ewm(alpha=.2).std()
        0         NaN
        1    0.707107
        2    0.995893
        3    1.277320
        dtype: float64
        """
        ),
        window_method="ewm",
        aggregation_description="(exponential weighted moment) standard deviation",
        agg_method="std",
    )
    def std(self, bias: bool = False, numeric_only: bool = False):
        if (
            numeric_only
            and self._selected_obj.ndim == 1
            and not is_numeric_dtype(self._selected_obj.dtype)
        ):
            # Raise directly so error message says std instead of var
            raise NotImplementedError(
                f"{type(self).__name__}.std does not implement numeric_only"
            )
        return zsqrt(self.var(bias=bias, numeric_only=numeric_only))
