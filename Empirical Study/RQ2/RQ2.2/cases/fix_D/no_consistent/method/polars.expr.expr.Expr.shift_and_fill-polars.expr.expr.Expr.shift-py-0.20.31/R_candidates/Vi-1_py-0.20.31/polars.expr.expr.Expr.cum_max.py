    def cum_max(self, *, reverse: bool = False) -> Self:
        """
        Get an array with the cumulative max computed at every element.

        Parameters
        ----------
        reverse
            Reverse the operation.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1, 3, 2]})
        >>> df.with_columns(
        ...     pl.col("a").cum_max().alias("cum_max"),
        ...     pl.col("a").cum_max(reverse=True).alias("cum_max_reverse"),
        ... )
        shape: (3, 3)
        ┌─────┬─────────┬─────────────────┐
        │ a   ┆ cum_max ┆ cum_max_reverse │
        │ --- ┆ ---     ┆ ---             │
        │ i64 ┆ i64     ┆ i64             │
        ╞═════╪═════════╪═════════════════╡
        │ 1   ┆ 1       ┆ 3               │
        │ 3   ┆ 3       ┆ 3               │
        │ 2   ┆ 3       ┆ 2               │
        └─────┴─────────┴─────────────────┘


        Null values are excluded, but can also be filled by calling `forward_fill`.

        >>> df = pl.DataFrame({"values": [None, 10, None, 8, 9, None, 16, None]})
        >>> df.with_columns(
        ...     pl.col("values").cum_max().alias("cum_max"),
        ...     pl.col("values").cum_max().forward_fill().alias("cum_max_all_filled"),
        ... )
        shape: (8, 3)
        ┌────────┬─────────┬────────────────────┐
        │ values ┆ cum_max ┆ cum_max_all_filled │
        │ ---    ┆ ---     ┆ ---                │
        │ i64    ┆ i64     ┆ i64                │
        ╞════════╪═════════╪════════════════════╡
        │ null   ┆ null    ┆ null               │
        │ 10     ┆ 10      ┆ 10                 │
        │ null   ┆ null    ┆ 10                 │
        │ 8      ┆ 10      ┆ 10                 │
        │ 9      ┆ 10      ┆ 10                 │
        │ null   ┆ null    ┆ 10                 │
        │ 16     ┆ 16      ┆ 16                 │
        │ null   ┆ null    ┆ 16                 │
        └────────┴─────────┴────────────────────┘
        """
        return self._from_pyexpr(self._pyexpr.cum_max(reverse))
