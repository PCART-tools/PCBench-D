    def tail(self, n: int | str | Expr = 5) -> Expr:
        """
        Slice the last `n` values of every sublist.

        Parameters
        ----------
        n
            Number of values to return for each sublist.

        Examples
        --------
        >>> s = pl.Series("a", [[1, 2, 3, 4], [10, 2, 1]])
        >>> s.list.tail(2)
        shape: (2,)
        Series: 'a' [list[i64]]
        [
            [3, 4]
            [2, 1]
        ]

        """
        n = parse_as_expression(n)
        return wrap_expr(self._pyexpr.list_tail(n))
