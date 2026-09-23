    def clip(
        self,
        lower_bound: NumericLiteral | TemporalLiteral | IntoExprColumn | None = None,
        upper_bound: NumericLiteral | TemporalLiteral | IntoExprColumn | None = None,
    ) -> Expr:
        """
        Set values outside the given boundaries to the boundary value.

        Parameters
        ----------
        lower_bound
            Lower bound. Accepts expression input.
            Non-expression inputs are parsed as literals.
        upper_bound
            Upper bound. Accepts expression input.
            Non-expression inputs are parsed as literals.

        See Also
        --------
        when

        Notes
        -----
        This method only works for numeric and temporal columns. To clip other data
        types, consider writing a `when-then-otherwise` expression. See :func:`when`.

        Examples
        --------
        Specifying both a lower and upper bound:

        >>> df = pl.DataFrame({"a": [-50, 5, 50, None]})
        >>> df.with_columns(clip=pl.col("a").clip(1, 10))
        shape: (4, 2)
        ┌──────┬──────┐
        │ a    ┆ clip │
        │ ---  ┆ ---  │
        │ i64  ┆ i64  │
        ╞══════╪══════╡
        │ -50  ┆ 1    │
        │ 5    ┆ 5    │
        │ 50   ┆ 10   │
        │ null ┆ null │
        └──────┴──────┘

        Specifying only a single bound:

        >>> df.with_columns(clip=pl.col("a").clip(upper_bound=10))
        shape: (4, 2)
        ┌──────┬──────┐
        │ a    ┆ clip │
        │ ---  ┆ ---  │
        │ i64  ┆ i64  │
        ╞══════╪══════╡
        │ -50  ┆ -50  │
        │ 5    ┆ 5    │
        │ 50   ┆ 10   │
        │ null ┆ null │
        └──────┴──────┘
        """
        if lower_bound is not None:
            lower_bound = parse_into_expression(lower_bound)
        if upper_bound is not None:
            upper_bound = parse_into_expression(upper_bound)
        return self._from_pyexpr(self._pyexpr.clip(lower_bound, upper_bound))
