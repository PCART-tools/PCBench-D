    @deprecate_renamed_function("name.map", moved=True, version="0.19.12")
    def map_alias(self, function: Callable[[str], str]) -> Self:
        """
        Rename the output of an expression by mapping a function over the root name.

        .. deprecated:: 0.19.12
            This method has been renamed to :func:`name.map`.

        Parameters
        ----------
        function
            Function that maps a root name to a new name.

        See Also
        --------
        keep_name
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
        return self.name.map(function)  # type: ignore[return-value]
