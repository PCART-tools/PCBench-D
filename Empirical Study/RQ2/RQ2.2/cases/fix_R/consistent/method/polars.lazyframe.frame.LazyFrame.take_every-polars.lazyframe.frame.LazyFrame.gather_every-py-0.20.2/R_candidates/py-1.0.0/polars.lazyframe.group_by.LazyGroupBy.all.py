    def all(self) -> LazyFrame:
        """
        Aggregate the groups into Series.

        Examples
        --------
        >>> ldf = pl.DataFrame(
        ...     {
        ...         "a": ["one", "two", "one", "two"],
        ...         "b": [1, 2, 3, 4],
        ...     }
        ... ).lazy()
        >>> ldf.group_by("a", maintain_order=True).all().collect()
        shape: (2, 2)
        ┌─────┬───────────┐
        │ a   ┆ b         │
        │ --- ┆ ---       │
        │ str ┆ list[i64] │
        ╞═════╪═══════════╡
        │ one ┆ [1, 3]    │
        │ two ┆ [2, 4]    │
        └─────┴───────────┘
        """
        return self.agg(F.all())
