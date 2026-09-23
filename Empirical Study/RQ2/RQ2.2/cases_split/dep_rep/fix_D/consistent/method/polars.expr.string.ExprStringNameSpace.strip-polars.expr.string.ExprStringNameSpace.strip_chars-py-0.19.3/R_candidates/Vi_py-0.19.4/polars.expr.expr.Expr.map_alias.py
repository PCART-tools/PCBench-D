    def map_alias(self, function: Callable[[str], str]) -> Self:
        """
        Rename the output of an expression by mapping a function over the root name.

        Parameters
        ----------
        function
            Function that maps a root name to a new name.

        See Also
        --------
        alias
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
        ...     pl.all().reverse().map_alias(lambda c: c.rstrip("_reverse").lower())
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
        return self._from_pyexpr(self._pyexpr.map_alias(function))
