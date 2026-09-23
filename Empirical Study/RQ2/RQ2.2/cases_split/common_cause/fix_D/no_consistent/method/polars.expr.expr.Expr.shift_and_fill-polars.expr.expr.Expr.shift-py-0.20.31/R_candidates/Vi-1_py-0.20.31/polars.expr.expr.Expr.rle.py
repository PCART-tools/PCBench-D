    def rle(self) -> Self:
        """
        Compress the column data using run-length encoding.

        Run-length encoding (RLE) encodes data by storing each *run* of identical values
        as a single value and its length.

        Returns
        -------
        Expr
            Expression of data type `Struct` with fields `lengths` of data type `Int32`
            and `values` of the original data type.

        See Also
        --------
        rle_id

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1, 1, 2, 1, None, 1, 3, 3]})
        >>> df.select(pl.col("a").rle()).unnest("a")
        shape: (6, 2)
        ┌─────────┬────────┐
        │ lengths ┆ values │
        │ ---     ┆ ---    │
        │ i32     ┆ i64    │
        ╞═════════╪════════╡
        │ 2       ┆ 1      │
        │ 1       ┆ 2      │
        │ 1       ┆ 1      │
        │ 1       ┆ null   │
        │ 1       ┆ 1      │
        │ 2       ┆ 3      │
        └─────────┴────────┘
        """
        return self._from_pyexpr(self._pyexpr.rle())
