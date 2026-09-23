    def keep_name(self) -> Self:
        """
        Keep the original root name of the expression.

        Notes
        -----
        Due to implementation constraints, this method can only be called as the last
        expression in a chain.

        See Also
        --------
        alias

        Examples
        --------
        Undo an alias operation.

        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 2],
        ...         "b": [3, 4],
        ...     }
        ... )
        >>> df.with_columns((pl.col("a") * 9).alias("c").keep_name())
        shape: (2, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 9   ┆ 3   │
        │ 18  ┆ 4   │
        └─────┴─────┘

        Prevent errors due to duplicate column names.

        >>> df.select((pl.lit(10) / pl.all()).keep_name())
        shape: (2, 2)
        ┌──────┬──────────┐
        │ a    ┆ b        │
        │ ---  ┆ ---      │
        │ f64  ┆ f64      │
        ╞══════╪══════════╡
        │ 10.0 ┆ 3.333333 │
        │ 5.0  ┆ 2.5      │
        └──────┴──────────┘

        """
        return self._from_pyexpr(self._pyexpr.keep_name())
