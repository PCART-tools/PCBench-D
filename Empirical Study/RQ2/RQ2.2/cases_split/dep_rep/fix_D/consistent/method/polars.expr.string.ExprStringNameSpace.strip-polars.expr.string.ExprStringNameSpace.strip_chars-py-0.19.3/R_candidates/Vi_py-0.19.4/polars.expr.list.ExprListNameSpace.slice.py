    def slice(
        self, offset: int | str | Expr, length: int | str | Expr | None = None
    ) -> Expr:
        """
        Slice every sublist.

        Parameters
        ----------
        offset
            Start index. Negative indexing is supported.
        length
            Length of the slice. If set to ``None`` (default), the slice is taken to the
            end of the list.

        Examples
        --------
        >>> s = pl.Series("a", [[1, 2, 3, 4], [10, 2, 1]])
        >>> s.list.slice(1, 2)
        shape: (2,)
        Series: 'a' [list[i64]]
        [
            [2, 3]
            [2, 1]
        ]

        """
        offset = parse_as_expression(offset)
        length = parse_as_expression(length)
        return wrap_expr(self._pyexpr.list_slice(offset, length))
