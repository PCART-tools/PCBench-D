    def unnest(self) -> DataFrame:
        """
        Convert this struct Series to a DataFrame with a separate column for each field.

        Examples
        --------
        >>> s = pl.Series([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        >>> s.struct.unnest()
        shape: (2, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 1   ┆ 2   │
        │ 3   ┆ 4   │
        └─────┴─────┘

        """
        return wrap_df(self._s.struct_unnest())
