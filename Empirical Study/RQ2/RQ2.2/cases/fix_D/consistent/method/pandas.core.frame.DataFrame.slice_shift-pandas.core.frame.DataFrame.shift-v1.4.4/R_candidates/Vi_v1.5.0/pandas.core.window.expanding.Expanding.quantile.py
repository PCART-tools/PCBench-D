    @doc(
        template_header,
        create_section_header("Parameters"),
        dedent(
            """
        quantile : float
            Quantile to compute. 0 <= quantile <= 1.
        interpolation : {{'linear', 'lower', 'higher', 'midpoint', 'nearest'}}
            This optional parameter specifies the interpolation method to use,
            when the desired quantile lies between two data points `i` and `j`:

                * linear: `i + (j - i) * fraction`, where `fraction` is the
                  fractional part of the index surrounded by `i` and `j`.
                * lower: `i`.
                * higher: `j`.
                * nearest: `i` or `j` whichever is nearest.
                * midpoint: (`i` + `j`) / 2.
        """
        ).replace("\n", "", 1),
        kwargs_numeric_only,
        kwargs_compat,
        create_section_header("Returns"),
        template_returns,
        create_section_header("See Also"),
        template_see_also[:-1],
        window_method="expanding",
        aggregation_description="quantile",
        agg_method="quantile",
    )
    def quantile(
        self,
        quantile: float,
        interpolation: QuantileInterpolation = "linear",
        numeric_only: bool = False,
        **kwargs,
    ):
        maybe_warn_args_and_kwargs(type(self), "quantile", None, kwargs)
        return super().quantile(
            quantile=quantile,
            interpolation=interpolation,
            numeric_only=numeric_only,
            **kwargs,
        )
