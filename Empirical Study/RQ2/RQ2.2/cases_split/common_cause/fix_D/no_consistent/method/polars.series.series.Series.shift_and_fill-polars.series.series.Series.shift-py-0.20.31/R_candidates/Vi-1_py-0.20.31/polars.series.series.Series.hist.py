    @unstable()
    def hist(
        self,
        bins: list[float] | None = None,
        *,
        bin_count: int | None = None,
        include_category: bool = True,
        include_breakpoint: bool = True,
    ) -> DataFrame:
        """
        Bin values into buckets and count their occurrences.

        .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

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

        Examples
        --------
        >>> a = pl.Series("a", [1, 3, 8, 8, 2, 1, 3])
        >>> a.hist(bin_count=4)
        shape: (5, 3)
        ┌─────────────┬─────────────┬───────┐
        │ break_point ┆ category    ┆ count │
        │ ---         ┆ ---         ┆ ---   │
        │ f64         ┆ cat         ┆ u32   │
        ╞═════════════╪═════════════╪═══════╡
        │ 0.0         ┆ (-inf, 0.0] ┆ 0     │
        │ 2.25        ┆ (0.0, 2.25] ┆ 3     │
        │ 4.5         ┆ (2.25, 4.5] ┆ 2     │
        │ 6.75        ┆ (4.5, 6.75] ┆ 0     │
        │ inf         ┆ (6.75, inf] ┆ 2     │
        └─────────────┴─────────────┴───────┘
        """
        out = (
            self.to_frame()
            .select_seq(
                F.col(self.name).hist(
                    bins=bins,
                    bin_count=bin_count,
                    include_category=include_category,
                    include_breakpoint=include_breakpoint,
                )
            )
            .to_series()
        )
        if not include_breakpoint and not include_category:
            return out.to_frame()
        else:
            return out.struct.unnest()
