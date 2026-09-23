    def to_dummies(
        self, *, separator: str = "_", drop_first: bool = False
    ) -> DataFrame:
        """
        Get dummy/indicator variables.

        Parameters
        ----------
        separator
            Separator/delimiter used when generating column names.
        drop_first
            Remove the first category from the variable being encoded.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> s.to_dummies()
        shape: (3, 3)
        ┌─────┬─────┬─────┐
        │ a_1 ┆ a_2 ┆ a_3 │
        │ --- ┆ --- ┆ --- │
        │ u8  ┆ u8  ┆ u8  │
        ╞═════╪═════╪═════╡
        │ 1   ┆ 0   ┆ 0   │
        │ 0   ┆ 1   ┆ 0   │
        │ 0   ┆ 0   ┆ 1   │
        └─────┴─────┴─────┘

        >>> s.to_dummies(drop_first=True)
        shape: (3, 2)
        ┌─────┬─────┐
        │ a_2 ┆ a_3 │
        │ --- ┆ --- │
        │ u8  ┆ u8  │
        ╞═════╪═════╡
        │ 0   ┆ 0   │
        │ 1   ┆ 0   │
        │ 0   ┆ 1   │
        └─────┴─────┘
        """
        return wrap_df(self._s.to_dummies(separator, drop_first))
