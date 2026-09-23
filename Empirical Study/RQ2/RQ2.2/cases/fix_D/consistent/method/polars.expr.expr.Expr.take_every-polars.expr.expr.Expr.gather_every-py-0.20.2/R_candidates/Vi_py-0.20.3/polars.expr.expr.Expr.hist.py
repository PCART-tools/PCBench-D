    def hist(
        self,
        bins: IntoExpr | None = None,
        *,
        bin_count: int | None = None,
        include_category: bool = False,
        include_breakpoint: bool = False,
    ) -> Self:
        """
        Bin values into buckets and count their occurrences.

        Parameters
        ----------
        bins
            Discretizations to make.
            If None given, we determine the boundaries based on the data.
        bin_count
            If no bins provided, this will be used to determine
            the distance of the bins
        include_breakpoint
            Include a column that indicates the upper breakpoint.
        include_category
            Include a column that shows the intervals as categories.

        Returns
        -------
        DataFrame

        Warnings
        --------
        This functionality is experimental and may change without it being considered a
        breaking change.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1, 3, 8, 8, 2, 1, 3]})
        >>> df.select(pl.col("a").hist(bins=[1, 2, 3]))
        shape: (4, 1)
        ┌─────┐
        │ a   │
        │ --- │
        │ u32 │
        ╞═════╡
        │ 2   │
        │ 1   │
        │ 2   │
        │ 2   │
        └─────┘
        >>> df.select(
        ...     pl.col("a").hist(
        ...         bins=[1, 2, 3], include_breakpoint=True, include_category=True
        ...     )
        ... )
        shape: (4, 1)
        ┌───────────────────────┐
        │ a                     │
        │ ---                   │
        │ struct[3]             │
        ╞═══════════════════════╡
        │ {1.0,"(-inf, 1.0]",2} │
        │ {2.0,"(1.0, 2.0]",1}  │
        │ {3.0,"(2.0, 3.0]",2}  │
        │ {inf,"(3.0, inf]",2}  │
        └───────────────────────┘

        """
        if bins is not None:
            if isinstance(bins, list):
                bins = pl.Series(bins)
            bins = parse_as_expression(bins)
        return self._from_pyexpr(
            self._pyexpr.hist(bins, bin_count, include_category, include_breakpoint)
        )
