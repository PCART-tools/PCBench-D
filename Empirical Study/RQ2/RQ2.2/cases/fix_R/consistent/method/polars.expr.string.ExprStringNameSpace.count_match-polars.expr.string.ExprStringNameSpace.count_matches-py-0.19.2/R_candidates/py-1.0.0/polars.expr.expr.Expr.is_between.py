    def is_between(
        self,
        lower_bound: IntoExpr,
        upper_bound: IntoExpr,
        closed: ClosedInterval = "both",
    ) -> Expr:
        """
        Check if this expression is between the given lower and upper bounds.

        Parameters
        ----------
        lower_bound
            Lower bound value. Accepts expression input. Strings are parsed as column
            names, other non-expression inputs are parsed as literals.
        upper_bound
            Upper bound value. Accepts expression input. Strings are parsed as column
            names, other non-expression inputs are parsed as literals.
        closed : {'both', 'left', 'right', 'none'}
            Define which sides of the interval are closed (inclusive).

        Notes
        -----
        If the value of the `lower_bound` is greater than that of the `upper_bound`
        then the result will be False, as no value can satisfy the condition.

        Returns
        -------
        Expr
            Expression of data type :class:`Boolean`.

        Examples
        --------
        >>> df = pl.DataFrame({"num": [1, 2, 3, 4, 5]})
        >>> df.with_columns(pl.col("num").is_between(2, 4).alias("is_between"))
        shape: (5, 2)
        ┌─────┬────────────┐
        │ num ┆ is_between │
        │ --- ┆ ---        │
        │ i64 ┆ bool       │
        ╞═════╪════════════╡
        │ 1   ┆ false      │
        │ 2   ┆ true       │
        │ 3   ┆ true       │
        │ 4   ┆ true       │
        │ 5   ┆ false      │
        └─────┴────────────┘

        Use the `closed` argument to include or exclude the values at the bounds:

        >>> df.with_columns(
        ...     pl.col("num").is_between(2, 4, closed="left").alias("is_between")
        ... )
        shape: (5, 2)
        ┌─────┬────────────┐
        │ num ┆ is_between │
        │ --- ┆ ---        │
        │ i64 ┆ bool       │
        ╞═════╪════════════╡
        │ 1   ┆ false      │
        │ 2   ┆ true       │
        │ 3   ┆ true       │
        │ 4   ┆ false      │
        │ 5   ┆ false      │
        └─────┴────────────┘

        You can also use strings as well as numeric/temporal values (note: ensure that
        string literals are wrapped with `lit` so as not to conflate them with
        column names):

        >>> df = pl.DataFrame({"a": ["a", "b", "c", "d", "e"]})
        >>> df.with_columns(
        ...     pl.col("a")
        ...     .is_between(pl.lit("a"), pl.lit("c"), closed="both")
        ...     .alias("is_between")
        ... )
        shape: (5, 2)
        ┌─────┬────────────┐
        │ a   ┆ is_between │
        │ --- ┆ ---        │
        │ str ┆ bool       │
        ╞═════╪════════════╡
        │ a   ┆ true       │
        │ b   ┆ true       │
        │ c   ┆ true       │
        │ d   ┆ false      │
        │ e   ┆ false      │
        └─────┴────────────┘

        Use column expressions as lower/upper bounds, comparing to a literal value:

        >>> df = pl.DataFrame({"a": [1, 2, 3, 4, 5], "b": [5, 4, 3, 2, 1]})
        >>> df.with_columns(
        ...     pl.lit(3).is_between(pl.col("a"), pl.col("b")).alias("between_ab")
        ... )
        shape: (5, 3)
        ┌─────┬─────┬────────────┐
        │ a   ┆ b   ┆ between_ab │
        │ --- ┆ --- ┆ ---        │
        │ i64 ┆ i64 ┆ bool       │
        ╞═════╪═════╪════════════╡
        │ 1   ┆ 5   ┆ true       │
        │ 2   ┆ 4   ┆ true       │
        │ 3   ┆ 3   ┆ true       │
        │ 4   ┆ 2   ┆ false      │
        │ 5   ┆ 1   ┆ false      │
        └─────┴─────┴────────────┘
        """
        lower_bound = parse_into_expression(lower_bound)
        upper_bound = parse_into_expression(upper_bound)

        return self._from_pyexpr(
            self._pyexpr.is_between(lower_bound, upper_bound, closed)
        )
