    def describe(self: DF) -> DF:
        """
        Summary statistics for a DataFrame.

        See Also
        --------
        glimpse

        Examples
        --------
        >>> from datetime import date
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1.0, 2.8, 3.0],
        ...         "b": [4, 5, None],
        ...         "c": [True, False, True],
        ...         "d": [None, "b", "c"],
        ...         "e": ["usd", "eur", None],
        ...         "f": [date(2020, 1, 1), date(2021, 1, 1), date(2022, 1, 1)],
        ...     }
        ... )
        >>> df.describe()
        shape: (7, 7)
        ┌────────────┬──────────┬──────────┬──────────┬──────┬──────┬────────────┐
        │ describe   ┆ a        ┆ b        ┆ c        ┆ d    ┆ e    ┆ f          │
        │ ---        ┆ ---      ┆ ---      ┆ ---      ┆ ---  ┆ ---  ┆ ---        │
        │ str        ┆ f64      ┆ f64      ┆ f64      ┆ str  ┆ str  ┆ str        │
        ╞════════════╪══════════╪══════════╪══════════╪══════╪══════╪════════════╡
        │ count      ┆ 3.0      ┆ 3.0      ┆ 3.0      ┆ 3    ┆ 3    ┆ 3          │
        │ null_count ┆ 0.0      ┆ 1.0      ┆ 0.0      ┆ 1    ┆ 1    ┆ 0          │
        │ mean       ┆ 2.266667 ┆ 4.5      ┆ 0.666667 ┆ null ┆ null ┆ null       │
        │ std        ┆ 1.101514 ┆ 0.707107 ┆ 0.57735  ┆ null ┆ null ┆ null       │
        │ min        ┆ 1.0      ┆ 4.0      ┆ 0.0      ┆ b    ┆ eur  ┆ 2020-01-01 │
        │ max        ┆ 3.0      ┆ 5.0      ┆ 1.0      ┆ c    ┆ usd  ┆ 2022-01-01 │
        │ median     ┆ 2.8      ┆ 4.5      ┆ 1.0      ┆ null ┆ null ┆ null       │
        └────────────┴──────────┴──────────┴──────────┴──────┴──────┴────────────┘

        """

        def describe_cast(stat: DF) -> DF:
            columns = []
            for i, s in enumerate(self.columns):
                if self[s].is_numeric() or self[s].is_boolean():
                    columns.append(stat[:, i].cast(float))
                else:
                    # for dates, strings, etc, we cast to string so that all
                    # statistics can be shown
                    columns.append(stat[:, i].cast(str))
            return self.__class__(columns)

        summary = self._from_pydf(
            pli.concat(
                [
                    describe_cast(
                        self.__class__({c: [len(self)] for c in self.columns})
                    ),
                    describe_cast(self.null_count()),
                    describe_cast(self.mean()),
                    describe_cast(self.std()),
                    describe_cast(self.min()),
                    describe_cast(self.max()),
                    describe_cast(self.median()),
                ]
            )._df
        )
        summary.insert_at_idx(
            0,
            pli.Series(
                "describe",
                ["count", "null_count", "mean", "std", "min", "max", "median"],
            ),
        )
        return summary
