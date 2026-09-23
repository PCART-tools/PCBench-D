    def rle_id(self) -> Self:
        """
        Map values to run IDs.

        Similar to RLE, but it maps each value to an ID corresponding to the run into
        which it falls. This is especially useful when you want to define groups by
        runs of identical values rather than the values themselves.


        Examples
        --------
        >>> df = pl.DataFrame(dict(a=[1, 2, 1, 1, 1], b=["x", "x", None, "y", "y"]))
        >>> # It works on structs of multiple values too!
        >>> df.with_columns(a_r=pl.col("a").rle_id(), ab_r=pl.struct("a", "b").rle_id())
        shape: (5, 4)
        ┌─────┬──────┬─────┬──────┐
        │ a   ┆ b    ┆ a_r ┆ ab_r │
        │ --- ┆ ---  ┆ --- ┆ ---  │
        │ i64 ┆ str  ┆ u32 ┆ u32  │
        ╞═════╪══════╪═════╪══════╡
        │ 1   ┆ x    ┆ 0   ┆ 0    │
        │ 2   ┆ x    ┆ 1   ┆ 1    │
        │ 1   ┆ null ┆ 2   ┆ 2    │
        │ 1   ┆ y    ┆ 2   ┆ 3    │
        │ 1   ┆ y    ┆ 2   ┆ 3    │
        └─────┴──────┴─────┴──────┘
        """
        return self._from_pyexpr(self._pyexpr.rle_id())
