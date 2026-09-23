    def cum_sum(self, *, reverse: bool = False) -> Self:
        """
        Get an array with the cumulative sum computed at every element.

        Parameters
        ----------
        reverse
            Reverse the operation.

        Notes
        -----
        Dtypes in {Int8, UInt8, Int16, UInt16} are cast to
        Int64 before summing to prevent overflow issues.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1, 2, 3, 4]})
        >>> df.with_columns(
        ...     pl.col("a").cum_sum().alias("cum_sum"),
        ...     pl.col("a").cum_sum(reverse=True).alias("cum_sum_reverse"),
        ... )
        shape: (4, 3)
        ┌─────┬─────────┬─────────────────┐
        │ a   ┆ cum_sum ┆ cum_sum_reverse │
        │ --- ┆ ---     ┆ ---             │
        │ i64 ┆ i64     ┆ i64             │
        ╞═════╪═════════╪═════════════════╡
        │ 1   ┆ 1       ┆ 10              │
        │ 2   ┆ 3       ┆ 9               │
        │ 3   ┆ 6       ┆ 7               │
        │ 4   ┆ 10      ┆ 4               │
        └─────┴─────────┴─────────────────┘

        Null values are excluded, but can also be filled by calling `forward_fill`.

        >>> df = pl.DataFrame({"values": [None, 10, None, 8, 9, None, 16, None]})
        >>> df.with_columns(
        ...     pl.col("values").cum_sum().alias("value_cum_sum"),
        ...     pl.col("values")
        ...     .cum_sum()
        ...     .forward_fill()
        ...     .alias("value_cum_sum_all_filled"),
        ... )
        shape: (8, 3)
        ┌────────┬───────────────┬──────────────────────────┐
        │ values ┆ value_cum_sum ┆ value_cum_sum_all_filled │
        │ ---    ┆ ---           ┆ ---                      │
        │ i64    ┆ i64           ┆ i64                      │
        ╞════════╪═══════════════╪══════════════════════════╡
        │ null   ┆ null          ┆ null                     │
        │ 10     ┆ 10            ┆ 10                       │
        │ null   ┆ null          ┆ 10                       │
        │ 8      ┆ 18            ┆ 18                       │
        │ 9      ┆ 27            ┆ 27                       │
        │ null   ┆ null          ┆ 27                       │
        │ 16     ┆ 43            ┆ 43                       │
        │ null   ┆ null          ┆ 43                       │
        └────────┴───────────────┴──────────────────────────┘

        """
        return self._from_pyexpr(self._pyexpr.cum_sum(reverse))
