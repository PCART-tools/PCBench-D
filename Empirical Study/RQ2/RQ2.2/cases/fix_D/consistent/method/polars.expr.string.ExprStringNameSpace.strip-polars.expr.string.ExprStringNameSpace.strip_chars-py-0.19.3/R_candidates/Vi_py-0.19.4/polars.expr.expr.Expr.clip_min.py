    def clip_min(
        self, lower_bound: NumericLiteral | TemporalLiteral | IntoExprColumn
    ) -> Self:
        """
        Clip (limit) the values in an array to a `min` boundary.

        Only works for physical numerical types.

        If you want to clip other dtypes, consider writing a "when, then, otherwise"
        expression. See :func:`when` for more information.

        Parameters
        ----------
        lower_bound
            Lower bound.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [-50, 5, None, 50]})
        >>> df.with_columns(pl.col("foo").clip_min(0).alias("foo_clipped"))
        shape: (4, 2)
        ┌──────┬─────────────┐
        │ foo  ┆ foo_clipped │
        │ ---  ┆ ---         │
        │ i64  ┆ i64         │
        ╞══════╪═════════════╡
        │ -50  ┆ 0           │
        │ 5    ┆ 5           │
        │ null ┆ null        │
        │ 50   ┆ 50          │
        └──────┴─────────────┘

        """
        lower_bound = parse_as_expression(lower_bound, str_as_lit=True)
        return self._from_pyexpr(self._pyexpr.clip_min(lower_bound))
