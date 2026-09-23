    def last(self) -> Expr:
        """
        Get the last value of the sub-arrays.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"a": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
        ...     schema={"a": pl.Array(pl.Int32, 3)},
        ... )
        >>> df.with_columns(last=pl.col("a").arr.last())
        shape: (3, 2)
        ┌───────────────┬──────┐
        │ a             ┆ last │
        │ ---           ┆ ---  │
        │ array[i32, 3] ┆ i32  │
        ╞═══════════════╪══════╡
        │ [1, 2, 3]     ┆ 3    │
        │ [4, 5, 6]     ┆ 6    │
        │ [7, 8, 9]     ┆ 9    │
        └───────────────┴──────┘

        """
        return self.get(-1, null_on_oob=True)
