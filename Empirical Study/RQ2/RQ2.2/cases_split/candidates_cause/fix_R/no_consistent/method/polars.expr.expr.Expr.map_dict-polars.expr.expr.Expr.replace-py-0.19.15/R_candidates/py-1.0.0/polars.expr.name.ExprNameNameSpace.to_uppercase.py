    def to_uppercase(self) -> Expr:
        """
        Make the root column name uppercase.

        Notes
        -----
        This will undo any previous renaming operations on the expression.

        Due to implementation constraints, this method can only be called as the last
        expression in a chain. Only one name operation per expression will work.
        Consider using `.name.map` for advanced renaming.

        See Also
        --------
        prefix
        suffix
        to_lowercase

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "ColX": [1, 2, 3],
        ...         "ColY": ["x", "y", "z"],
        ...     }
        ... )
        >>> df.with_columns(pl.all().name.to_uppercase())
        shape: (3, 4)
        ┌──────┬──────┬──────┬──────┐
        │ ColX ┆ ColY ┆ COLX ┆ COLY │
        │ ---  ┆ ---  ┆ ---  ┆ ---  │
        │ i64  ┆ str  ┆ i64  ┆ str  │
        ╞══════╪══════╪══════╪══════╡
        │ 1    ┆ x    ┆ 1    ┆ x    │
        │ 2    ┆ y    ┆ 2    ┆ y    │
        │ 3    ┆ z    ┆ 3    ┆ z    │
        └──────┴──────┴──────┴──────┘
        """
        return self._from_pyexpr(self._pyexpr.name_to_uppercase())
