    def with_row_index(self, name: str = "index", offset: int = 0) -> DataFrame:
        """
        Add a row index as the first column in the DataFrame.

        Parameters
        ----------
        name
            Name of the index column.
        offset
            Start the index at this offset. Cannot be negative.

        Notes
        -----
        The resulting column does not have any special properties. It is a regular
        column of type `UInt32` (or `UInt64` in `polars-u64-idx`).

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 3, 5],
        ...         "b": [2, 4, 6],
        ...     }
        ... )
        >>> df.with_row_index()
        shape: (3, 3)
        ┌───────┬─────┬─────┐
        │ index ┆ a   ┆ b   │
        │ ---   ┆ --- ┆ --- │
        │ u32   ┆ i64 ┆ i64 │
        ╞═══════╪═════╪═════╡
        │ 0     ┆ 1   ┆ 2   │
        │ 1     ┆ 3   ┆ 4   │
        │ 2     ┆ 5   ┆ 6   │
        └───────┴─────┴─────┘
        >>> df.with_row_index("id", offset=1000)
        shape: (3, 3)
        ┌──────┬─────┬─────┐
        │ id   ┆ a   ┆ b   │
        │ ---  ┆ --- ┆ --- │
        │ u32  ┆ i64 ┆ i64 │
        ╞══════╪═════╪═════╡
        │ 1000 ┆ 1   ┆ 2   │
        │ 1001 ┆ 3   ┆ 4   │
        │ 1002 ┆ 5   ┆ 6   │
        └──────┴─────┴─────┘

        An index column can also be created using the expressions :func:`int_range`
        and :func:`len`.

        >>> df.select(
        ...     pl.int_range(pl.len(), dtype=pl.UInt32).alias("index"),
        ...     pl.all(),
        ... )
        shape: (3, 3)
        ┌───────┬─────┬─────┐
        │ index ┆ a   ┆ b   │
        │ ---   ┆ --- ┆ --- │
        │ u32   ┆ i64 ┆ i64 │
        ╞═══════╪═════╪═════╡
        │ 0     ┆ 1   ┆ 2   │
        │ 1     ┆ 3   ┆ 4   │
        │ 2     ┆ 5   ┆ 6   │
        └───────┴─────┴─────┘
        """
        try:
            return self._from_pydf(self._df.with_row_index(name, offset))
        except OverflowError:
            issue = "negative" if offset < 0 else "greater than the maximum index value"
            msg = f"`offset` input for `with_row_index` cannot be {issue}, got {offset}"
            raise ValueError(msg) from None
