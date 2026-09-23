    def shift(self, periods: int | IntoExprColumn = 1) -> Expr:
        """
        Shift values by the given period.

        Parameters
        ----------
        periods
            Number of places to shift (may be negative).

        Examples
        --------
        >>> s = pl.Series("a", [[1, 2, 3, 4], [10, 2, 1]])
        >>> s.list.shift()
        shape: (2,)
        Series: 'a' [list[i64]]
        [
            [null, 1, … 3]
            [null, 10, 2]
        ]

        """
        periods = parse_as_expression(periods)
        return wrap_expr(self._pyexpr.list_shift(periods))
