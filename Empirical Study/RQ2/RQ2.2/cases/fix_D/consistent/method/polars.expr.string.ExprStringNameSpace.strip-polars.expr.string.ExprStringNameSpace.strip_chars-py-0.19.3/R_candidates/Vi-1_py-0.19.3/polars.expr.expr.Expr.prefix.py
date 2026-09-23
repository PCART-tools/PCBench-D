    def prefix(self, prefix: str) -> Self:
        """
        Add a prefix to the root column name of the expression.

        Parameters
        ----------
        prefix
            Prefix to add to the root column name.

        Notes
        -----
        This will undo any previous renaming operations on the expression.

        Due to implementation constraints, this method can only be called as the last
        expression in a chain.

        See Also
        --------
        suffix

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 2, 3],
        ...         "b": ["x", "y", "z"],
        ...     }
        ... )
        >>> df.with_columns(pl.all().reverse().prefix("reverse_"))
        shape: (3, 4)
        ┌─────┬─────┬───────────┬───────────┐
        │ a   ┆ b   ┆ reverse_a ┆ reverse_b │
        │ --- ┆ --- ┆ ---       ┆ ---       │
        │ i64 ┆ str ┆ i64       ┆ str       │
        ╞═════╪═════╪═══════════╪═══════════╡
        │ 1   ┆ x   ┆ 3         ┆ z         │
        │ 2   ┆ y   ┆ 2         ┆ y         │
        │ 3   ┆ z   ┆ 1         ┆ x         │
        └─────┴─────┴───────────┴───────────┘

        """
        return self._from_pyexpr(self._pyexpr.prefix(prefix))
