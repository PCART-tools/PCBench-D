    @deprecate_function("Use `clip` instead.", version="0.19.12")
    def clip_max(
        self, upper_bound: NumericLiteral | TemporalLiteral | IntoExprColumn
    ) -> Self:
        """
        Clip (limit) the values in an array to a `max` boundary.

        .. deprecated:: 0.19.12
            Use :func:`clip` instead.

        Parameters
        ----------
        upper_bound
            Upper bound.
        """
        return self.clip(upper_bound=upper_bound)
