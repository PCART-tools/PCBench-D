    def has_nulls(self) -> Expr:
        """
        Check whether the expression contains one or more null values.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [None, 1, None],
        ...         "b": [10, None, 300],
        ...         "c": [350, 650, 850],
        ...     }
        ... )
        >>> df.select(pl.all().has_nulls())
        shape: (1, 3)
        ┌──────┬──────┬───────┐
        │ a    ┆ b    ┆ c     │
        │ ---  ┆ ---  ┆ ---   │
        │ bool ┆ bool ┆ bool  │
        ╞══════╪══════╪═══════╡
        │ true ┆ true ┆ false │
        └──────┴──────┴───────┘
        """
        return self.null_count() > 0
