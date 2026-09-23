    def alias(self, name: str) -> Self:
        """
        Rename the expression.

        Parameters
        ----------
        name
            The new name.

        See Also
        --------
        map
        prefix
        suffix

        Examples
        --------
        Rename an expression to avoid overwriting an existing column.

        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 2, 3],
        ...         "b": ["x", "y", "z"],
        ...     }
        ... )
        >>> df.with_columns(
        ...     pl.col("a") + 10,
        ...     pl.col("b").str.to_uppercase().alias("c"),
        ... )
        shape: (3, 3)
        ┌─────┬─────┬─────┐
        │ a   ┆ b   ┆ c   │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ str ┆ str │
        ╞═════╪═════╪═════╡
        │ 11  ┆ x   ┆ X   │
        │ 12  ┆ y   ┆ Y   │
        │ 13  ┆ z   ┆ Z   │
        └─────┴─────┴─────┘

        Overwrite the default name of literal columns to prevent errors due to duplicate
        column names.

        >>> df.with_columns(
        ...     pl.lit(True).alias("c"),
        ...     pl.lit(4.0).alias("d"),
        ... )
        shape: (3, 4)
        ┌─────┬─────┬──────┬─────┐
        │ a   ┆ b   ┆ c    ┆ d   │
        │ --- ┆ --- ┆ ---  ┆ --- │
        │ i64 ┆ str ┆ bool ┆ f64 │
        ╞═════╪═════╪══════╪═════╡
        │ 1   ┆ x   ┆ true ┆ 4.0 │
        │ 2   ┆ y   ┆ true ┆ 4.0 │
        │ 3   ┆ z   ┆ true ┆ 4.0 │
        └─────┴─────┴──────┴─────┘

        """
        return self._from_pyexpr(self._pyexpr.alias(name))
