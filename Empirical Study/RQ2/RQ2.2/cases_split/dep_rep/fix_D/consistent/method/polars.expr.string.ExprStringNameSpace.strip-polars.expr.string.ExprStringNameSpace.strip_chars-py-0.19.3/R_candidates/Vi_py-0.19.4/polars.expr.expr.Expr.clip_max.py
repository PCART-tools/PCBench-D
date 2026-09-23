    def clip_max(
        self, upper_bound: NumericLiteral | TemporalLiteral | IntoExprColumn
    ) -> Self:
        """
        Clip (limit) the values in an array to a `max` boundary.

        Only works for physical numerical types.

        If you want to clip other dtypes, consider writing a "when, then, otherwise"
        expression. See :func:`when` for more information.

        Parameters
        ----------
        upper_bound
            Upper bound.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [-50, 5, None, 50]})
        >>> df.with_columns(pl.col("foo").clip_max(0).alias("foo_clipped"))
        shape: (4, 2)
        ┌──────┬─────────────┐
        │ foo  ┆ foo_clipped │
        │ ---  ┆ ---         │
        │ i64  ┆ i64         │
        ╞══════╪═════════════╡
        │ -50  ┆ -50         │
        │ 5    ┆ 0           │
        │ null ┆ null        │
        │ 50   ┆ 0           │
        └──────┴─────────────┘

        """
        upper_bound = parse_as_expression(upper_bound, str_as_lit=True)
        return self._from_pyexpr(self._pyexpr.clip_max(upper_bound))
