    def with_context(self, other: Self | list[Self]) -> Self:
        """
        Add an external context to the computation graph.

        This allows expressions to also access columns from DataFrames
        that are not part of this one.

        Parameters
        ----------
        other
            Lazy DataFrame to join with.

        Examples
        --------
        >>> lf = pl.LazyFrame({"a": [1, 2, 3], "b": ["a", "c", None]})
        >>> lf_other = pl.LazyFrame({"c": ["foo", "ham"]})
        >>> lf.with_context(lf_other).select(
        ...     pl.col("b") + pl.col("c").first()
        ... ).collect()
        shape: (3, 1)
        ┌──────┐
        │ b    │
        │ ---  │
        │ str  │
        ╞══════╡
        │ afoo │
        │ cfoo │
        │ null │
        └──────┘

        Fill nulls with the median from another DataFrame:

        >>> train_lf = pl.LazyFrame(
        ...     {"feature_0": [-1.0, 0, 1], "feature_1": [-1.0, 0, 1]}
        ... )
        >>> test_lf = pl.LazyFrame(
        ...     {"feature_0": [-1.0, None, 1], "feature_1": [-1.0, 0, 1]}
        ... )
        >>> test_lf.with_context(
        ...     train_lf.select(pl.all().name.suffix("_train"))
        ... ).select(
        ...     pl.col("feature_0").fill_null(pl.col("feature_0_train").median())
        ... ).collect()
        shape: (3, 1)
        ┌───────────┐
        │ feature_0 │
        │ ---       │
        │ f64       │
        ╞═══════════╡
        │ -1.0      │
        │ 0.0       │
        │ 1.0       │
        └───────────┘

        """
        if not isinstance(other, list):
            other = [other]

        return self._from_pyldf(self._ldf.with_context([lf._ldf for lf in other]))
