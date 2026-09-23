    @deprecate_function(
        "Use `with_row_index` instead."
        " Note that the default column name has changed from 'row_nr' to 'index'.",
        version="0.20.4",
    )
    def with_row_count(self, name: str = "row_nr", offset: int = 0) -> LazyFrame:
        """
        Add a column at index 0 that counts the rows.

        .. deprecated:: 0.20.4
            Use :meth:`with_row_index` instead.
            Note that the default column name has changed from 'row_nr' to 'index'.

        Parameters
        ----------
        name
            Name of the column to add.
        offset
            Start the row count at this offset.

        Warnings
        --------
        This can have a negative effect on query performance.
        This may, for instance, block predicate pushdown optimization.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": [1, 3, 5],
        ...         "b": [2, 4, 6],
        ...     }
        ... )
        >>> lf.with_row_count().collect()  # doctest: +SKIP
        shape: (3, 3)
        ┌────────┬─────┬─────┐
        │ row_nr ┆ a   ┆ b   │
        │ ---    ┆ --- ┆ --- │
        │ u32    ┆ i64 ┆ i64 │
        ╞════════╪═════╪═════╡
        │ 0      ┆ 1   ┆ 2   │
        │ 1      ┆ 3   ┆ 4   │
        │ 2      ┆ 5   ┆ 6   │
        └────────┴─────┴─────┘
        """
        return self.with_row_index(name, offset)
