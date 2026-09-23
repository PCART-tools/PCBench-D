    def keep(self) -> Expr:
        """
        Keep the original root name of the expression.

        Notes
        -----
        This will undo any previous renaming operations on the expression.

        Due to implementation constraints, this method can only be called as the last
        expression in a chain. Only one name operation per expression will work.
        Consider using `.name.map` for advanced renaming.

        See Also
        --------
        Expr.alias
        map

        Examples
        --------
        Prevent errors due to potential duplicate column names.

        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 2],
        ...         "b": [3, 4],
        ...     }
        ... )
        >>> df.select((pl.lit(10) / pl.all()).name.keep())
        shape: (2, 2)
        ┌──────┬──────────┐
        │ a    ┆ b        │
        │ ---  ┆ ---      │
        │ f64  ┆ f64      │
        ╞══════╪══════════╡
        │ 10.0 ┆ 3.333333 │
        │ 5.0  ┆ 2.5      │
        └──────┴──────────┘

        Undo an alias operation.

        >>> df.with_columns((pl.col("a") * 9).alias("c").name.keep())
        shape: (2, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 9   ┆ 3   │
        │ 18  ┆ 4   │
        └─────┴─────┘
        """
        return self._from_pyexpr(self._pyexpr.name_keep())
