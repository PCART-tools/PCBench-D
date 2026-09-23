    def first(self) -> Expr:
        """
        Get the first value of the sub-arrays.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"a": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
        ...     schema={"a": pl.Array(pl.Int32, 3)},
        ... )
        >>> df.with_columns(first=pl.col("a").arr.first())
        shape: (3, 2)
        ┌───────────────┬───────┐
        │ a             ┆ first │
        │ ---           ┆ ---   │
        │ array[i32, 3] ┆ i32   │
        ╞═══════════════╪═══════╡
        │ [1, 2, 3]     ┆ 1     │
        │ [4, 5, 6]     ┆ 4     │
        │ [7, 8, 9]     ┆ 7     │
        └───────────────┴───────┘

        """
        return self.get(0, null_on_oob=True)
