    def rename(self, mapping: dict[str, str]) -> Self:
        """
        Rename column names.

        Parameters
        ----------
        mapping
            Key value pairs that map from old name to new name.

        Notes
        -----
        If existing names are swapped (e.g. 'A' points to 'B' and 'B' points to 'A'),
        polars will block projection and predicate pushdowns at this node.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6, 7, 8],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> lf.rename({"foo": "apple"}).collect()
        shape: (3, 3)
        ┌───────┬─────┬─────┐
        │ apple ┆ bar ┆ ham │
        │ ---   ┆ --- ┆ --- │
        │ i64   ┆ i64 ┆ str │
        ╞═══════╪═════╪═════╡
        │ 1     ┆ 6   ┆ a   │
        │ 2     ┆ 7   ┆ b   │
        │ 3     ┆ 8   ┆ c   │
        └───────┴─────┴─────┘

        """
        existing = list(mapping.keys())
        new = list(mapping.values())
        return self._from_pyldf(self._ldf.rename(existing, new))
