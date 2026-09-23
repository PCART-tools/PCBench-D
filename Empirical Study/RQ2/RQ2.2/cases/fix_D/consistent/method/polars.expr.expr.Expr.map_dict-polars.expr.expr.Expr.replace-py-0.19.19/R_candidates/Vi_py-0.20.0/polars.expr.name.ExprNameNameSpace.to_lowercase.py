    def to_lowercase(self) -> Expr:
        """
        Make the root column name lowercase.

        Notes
        -----
        Due to implementation constraints, this method can only be called as the last
        expression in a chain.

        See Also
        --------
        prefix
        suffix
        to_uppercase

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "ColX": [1, 2, 3],
        ...         "ColY": ["x", "y", "z"],
        ...     }
        ... )
        >>> df.with_columns(pl.all().name.to_lowercase())
        shape: (3, 4)
        ┌──────┬──────┬──────┬──────┐
        │ ColX ┆ ColY ┆ colx ┆ coly │
        │ ---  ┆ ---  ┆ ---  ┆ ---  │
        │ i64  ┆ str  ┆ i64  ┆ str  │
        ╞══════╪══════╪══════╪══════╡
        │ 1    ┆ x    ┆ 1    ┆ x    │
        │ 2    ┆ y    ┆ 2    ┆ y    │
        │ 3    ┆ z    ┆ 3    ┆ z    │
        └──────┴──────┴──────┴──────┘

        """
        return self._from_pyexpr(self._pyexpr.name_to_lowercase())
