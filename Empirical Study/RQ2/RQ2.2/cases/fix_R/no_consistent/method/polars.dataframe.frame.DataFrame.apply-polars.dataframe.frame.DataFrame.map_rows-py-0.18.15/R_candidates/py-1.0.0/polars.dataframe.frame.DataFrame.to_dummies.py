    def to_dummies(
        self,
        columns: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None,
        *,
        separator: str = "_",
        drop_first: bool = False,
    ) -> DataFrame:
        """
        Convert categorical variables into dummy/indicator variables.

        Parameters
        ----------
        columns
            Column name(s) or selector(s) that should be converted to dummy
            variables. If set to `None` (default), convert all columns.
        separator
            Separator/delimiter used when generating column names.
        drop_first
            Remove the first category from the variables being encoded.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2],
        ...         "bar": [3, 4],
        ...         "ham": ["a", "b"],
        ...     }
        ... )
        >>> df.to_dummies()
        shape: (2, 6)
        ┌───────┬───────┬───────┬───────┬───────┬───────┐
        │ foo_1 ┆ foo_2 ┆ bar_3 ┆ bar_4 ┆ ham_a ┆ ham_b │
        │ ---   ┆ ---   ┆ ---   ┆ ---   ┆ ---   ┆ ---   │
        │ u8    ┆ u8    ┆ u8    ┆ u8    ┆ u8    ┆ u8    │
        ╞═══════╪═══════╪═══════╪═══════╪═══════╪═══════╡
        │ 1     ┆ 0     ┆ 1     ┆ 0     ┆ 1     ┆ 0     │
        │ 0     ┆ 1     ┆ 0     ┆ 1     ┆ 0     ┆ 1     │
        └───────┴───────┴───────┴───────┴───────┴───────┘

        >>> df.to_dummies(drop_first=True)
        shape: (2, 3)
        ┌───────┬───────┬───────┐
        │ foo_2 ┆ bar_4 ┆ ham_b │
        │ ---   ┆ ---   ┆ ---   │
        │ u8    ┆ u8    ┆ u8    │
        ╞═══════╪═══════╪═══════╡
        │ 0     ┆ 0     ┆ 0     │
        │ 1     ┆ 1     ┆ 1     │
        └───────┴───────┴───────┘

        >>> import polars.selectors as cs
        >>> df.to_dummies(cs.integer(), separator=":")
        shape: (2, 5)
        ┌───────┬───────┬───────┬───────┬─────┐
        │ foo:1 ┆ foo:2 ┆ bar:3 ┆ bar:4 ┆ ham │
        │ ---   ┆ ---   ┆ ---   ┆ ---   ┆ --- │
        │ u8    ┆ u8    ┆ u8    ┆ u8    ┆ str │
        ╞═══════╪═══════╪═══════╪═══════╪═════╡
        │ 1     ┆ 0     ┆ 1     ┆ 0     ┆ a   │
        │ 0     ┆ 1     ┆ 0     ┆ 1     ┆ b   │
        └───────┴───────┴───────┴───────┴─────┘

        >>> df.to_dummies(cs.integer(), drop_first=True, separator=":")
        shape: (2, 3)
        ┌───────┬───────┬─────┐
        │ foo:2 ┆ bar:4 ┆ ham │
        │ ---   ┆ ---   ┆ --- │
        │ u8    ┆ u8    ┆ str │
        ╞═══════╪═══════╪═════╡
        │ 0     ┆ 0     ┆ a   │
        │ 1     ┆ 1     ┆ b   │
        └───────┴───────┴─────┘
        """
        if columns is not None:
            columns = _expand_selectors(self, columns)
        return self._from_pydf(self._df.to_dummies(columns, separator, drop_first))
