    def rle_id(self) -> Expr:
        """
        Get a distinct integer ID for each run of identical values.

        The ID starts at 0 and increases by one each time the value of the column
        changes.

        Returns
        -------
        Expr
            Expression of data type `UInt32`.

        See Also
        --------
        rle

        Notes
        -----
        This functionality is especially useful for defining a new group for every time
        a column's value changes, rather than for every distinct value of that column.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 2, 1, 1, 1],
        ...         "b": ["x", "x", None, "y", "y"],
        ...     }
        ... )
        >>> df.with_columns(
        ...     rle_id_a=pl.col("a").rle_id(),
        ...     rle_id_ab=pl.struct("a", "b").rle_id(),
        ... )
        shape: (5, 4)
        ┌─────┬──────┬──────────┬───────────┐
        │ a   ┆ b    ┆ rle_id_a ┆ rle_id_ab │
        │ --- ┆ ---  ┆ ---      ┆ ---       │
        │ i64 ┆ str  ┆ u32      ┆ u32       │
        ╞═════╪══════╪══════════╪═══════════╡
        │ 1   ┆ x    ┆ 0        ┆ 0         │
        │ 2   ┆ x    ┆ 1        ┆ 1         │
        │ 1   ┆ null ┆ 2        ┆ 2         │
        │ 1   ┆ y    ┆ 2        ┆ 3         │
        │ 1   ┆ y    ┆ 2        ┆ 3         │
        └─────┴──────┴──────────┴───────────┘
        """
        return self._from_pyexpr(self._pyexpr.rle_id())
