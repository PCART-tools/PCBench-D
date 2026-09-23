    def suffix(self, suffix: str) -> Expr:
        """
        Add a suffix to the root column name of the expression.

        Parameters
        ----------
        suffix
            Suffix to add to the root column name.

        Notes
        -----
        This will undo any previous renaming operations on the expression.

        Due to implementation constraints, this method can only be called as the last
        expression in a chain. Only one name operation per expression will work.
        Consider using `.name.map` for advanced renaming.

        See Also
        --------
        prefix

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 2, 3],
        ...         "b": ["x", "y", "z"],
        ...     }
        ... )
        >>> df.with_columns(pl.all().reverse().name.suffix("_reverse"))
        shape: (3, 4)
        ┌─────┬─────┬───────────┬───────────┐
        │ a   ┆ b   ┆ a_reverse ┆ b_reverse │
        │ --- ┆ --- ┆ ---       ┆ ---       │
        │ i64 ┆ str ┆ i64       ┆ str       │
        ╞═════╪═════╪═══════════╪═══════════╡
        │ 1   ┆ x   ┆ 3         ┆ z         │
        │ 2   ┆ y   ┆ 2         ┆ y         │
        │ 3   ┆ z   ┆ 1         ┆ x         │
        └─────┴─────┴───────────┴───────────┘
        """
        return self._from_pyexpr(self._pyexpr.name_suffix(suffix))
