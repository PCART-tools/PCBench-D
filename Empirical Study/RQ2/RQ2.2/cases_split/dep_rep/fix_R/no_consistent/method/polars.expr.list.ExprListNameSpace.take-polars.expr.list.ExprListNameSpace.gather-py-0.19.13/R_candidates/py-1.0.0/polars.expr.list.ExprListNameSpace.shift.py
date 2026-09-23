    def shift(self, n: int | IntoExprColumn = 1) -> Expr:
        """
        Shift list values by the given number of indices.

        Parameters
        ----------
        n
            Number of indices to shift forward. If a negative value is passed, values
            are shifted in the opposite direction instead.

        Notes
        -----
        This method is similar to the `LAG` operation in SQL when the value for `n`
        is positive. With a negative value for `n`, it is similar to `LEAD`.

        Examples
        --------
        By default, list values are shifted forward by one index.

        >>> df = pl.DataFrame({"a": [[1, 2, 3], [4, 5]]})
        >>> df.with_columns(shift=pl.col("a").list.shift())
        shape: (2, 2)
        ┌───────────┬──────────────┐
        │ a         ┆ shift        │
        │ ---       ┆ ---          │
        │ list[i64] ┆ list[i64]    │
        ╞═══════════╪══════════════╡
        │ [1, 2, 3] ┆ [null, 1, 2] │
        │ [4, 5]    ┆ [null, 4]    │
        └───────────┴──────────────┘

        Pass a negative value to shift in the opposite direction instead.

        >>> df.with_columns(shift=pl.col("a").list.shift(-2))
        shape: (2, 2)
        ┌───────────┬─────────────────┐
        │ a         ┆ shift           │
        │ ---       ┆ ---             │
        │ list[i64] ┆ list[i64]       │
        ╞═══════════╪═════════════════╡
        │ [1, 2, 3] ┆ [3, null, null] │
        │ [4, 5]    ┆ [null, null]    │
        └───────────┴─────────────────┘
        """
        n = parse_into_expression(n)
        return wrap_expr(self._pyexpr.list_shift(n))
