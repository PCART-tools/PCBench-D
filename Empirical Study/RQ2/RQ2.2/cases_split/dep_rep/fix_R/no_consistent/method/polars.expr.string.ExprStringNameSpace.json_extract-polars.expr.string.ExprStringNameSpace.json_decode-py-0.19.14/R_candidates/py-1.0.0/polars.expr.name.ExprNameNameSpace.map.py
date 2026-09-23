    def map(self, function: Callable[[str], str]) -> Expr:
        """
        Rename the output of an expression by mapping a function over the root name.

        Notes
        -----
        This will undo any previous renaming operations on the expression.

        Due to implementation constraints, this method can only be called as the last
        expression in a chain. Only one name operation per expression will work.


        Parameters
        ----------
        function
            Function that maps a root name to a new name.

        See Also
        --------
        keep
        prefix
        suffix

        Examples
        --------
        Remove a common suffix and convert to lower case.

        >>> df = pl.DataFrame(
        ...     {
        ...         "A_reverse": [3, 2, 1],
        ...         "B_reverse": ["z", "y", "x"],
        ...     }
        ... )
        >>> df.with_columns(
        ...     pl.all().reverse().name.map(lambda c: c.rstrip("_reverse").lower())
        ... )
        shape: (3, 4)
        ┌───────────┬───────────┬─────┬─────┐
        │ A_reverse ┆ B_reverse ┆ a   ┆ b   │
        │ ---       ┆ ---       ┆ --- ┆ --- │
        │ i64       ┆ str       ┆ i64 ┆ str │
        ╞═══════════╪═══════════╪═════╪═════╡
        │ 3         ┆ z         ┆ 1   ┆ x   │
        │ 2         ┆ y         ┆ 2   ┆ y   │
        │ 1         ┆ x         ┆ 3   ┆ z   │
        └───────────┴───────────┴─────┴─────┘
        """
        return self._from_pyexpr(self._pyexpr.name_map(function))
