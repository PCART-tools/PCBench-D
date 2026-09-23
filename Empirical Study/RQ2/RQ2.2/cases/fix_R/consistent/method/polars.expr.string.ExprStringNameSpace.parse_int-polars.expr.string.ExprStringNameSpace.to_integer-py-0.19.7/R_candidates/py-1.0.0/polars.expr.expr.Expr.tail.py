    def tail(self, n: int | Expr = 10) -> Expr:
        """
        Get the last `n` rows.

        Parameters
        ----------
        n
            Number of rows to return.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, 2, 3, 4, 5, 6, 7]})
        >>> df.tail(3)
        shape: (3, 1)
        ┌─────┐
        │ foo │
        │ --- │
        │ i64 │
        ╞═════╡
        │ 5   │
        │ 6   │
        │ 7   │
        └─────┘
        """
        # This cast enables tail with expressions that return unsigned integers,
        # for which negate otherwise raises InvalidOperationError.
        offset = -self._from_pyexpr(
            parse_into_expression(n).cast(Int64, strict=False, wrap_numerical=True)
        )
        return self.slice(offset, n)
