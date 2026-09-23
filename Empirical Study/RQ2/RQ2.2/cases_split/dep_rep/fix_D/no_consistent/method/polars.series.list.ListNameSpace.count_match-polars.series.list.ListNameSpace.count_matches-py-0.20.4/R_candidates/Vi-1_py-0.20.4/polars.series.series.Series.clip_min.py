    @deprecate_function("Use `clip` instead.", version="0.19.12")
    def clip_min(
        self, lower_bound: NumericLiteral | TemporalLiteral | IntoExprColumn
    ) -> Series:
        """
        Clip (limit) the values in an array to a `min` boundary.

        .. deprecated:: 0.19.12
            Use :func:`clip` instead.

        Parameters
        ----------
        lower_bound
            Lower bound.
        """
