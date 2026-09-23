    def describe(
        self, percentiles: Sequence[float] | float | None = (0.25, 0.50, 0.75)
    ) -> DataFrame:
        """
        Quick summary statistics of a Series.

        Series with mixed datatypes will return summary statistics for the datatype of
        the first value.

        Parameters
        ----------
        percentiles
            One or more percentiles to include in the summary statistics (if the
            Series has a numeric dtype). All values must be in the range `[0, 1]`.

        Notes
        -----
        The median is included by default as the 50% percentile.

        Returns
        -------
        DataFrame
            Mapping with summary statistics of a Series.

        Examples
        --------
        >>> s = pl.Series([1, 2, 3, 4, 5])
        >>> s.describe()
        shape: (9, 2)
        ┌────────────┬──────────┐
        │ statistic  ┆ value    │
        │ ---        ┆ ---      │
        │ str        ┆ f64      │
        ╞════════════╪══════════╡
        │ count      ┆ 5.0      │
        │ null_count ┆ 0.0      │
        │ mean       ┆ 3.0      │
        │ std        ┆ 1.581139 │
        │ min        ┆ 1.0      │
        │ 25%        ┆ 2.0      │
        │ 50%        ┆ 3.0      │
        │ 75%        ┆ 4.0      │
        │ max        ┆ 5.0      │
        └────────────┴──────────┘

        Non-numeric data types may not have all statistics available.

        >>> s = pl.Series(["a", "a", None, "b", "c"])
        >>> s.describe()
        shape: (3, 2)
        ┌────────────┬───────┐
        │ statistic  ┆ value │
        │ ---        ┆ ---   │
        │ str        ┆ i64   │
        ╞════════════╪═══════╡
        │ count      ┆ 4     │
        │ null_count ┆ 1     │
        │ unique     ┆ 4     │
        └────────────┴───────┘

        """
        stats: dict[str, PythonLiteral | None]
        stats_dtype: PolarsDataType

        if self.dtype.is_numeric():
            stats_dtype = Float64
            stats = {
                "count": self.count(),
                "null_count": self.null_count(),
                "mean": self.mean(),
                "std": self.std(),
                "min": self.min(),
            }
            for p in parse_percentiles(percentiles):
                stats[f"{p:.0%}"] = self.quantile(p)
            stats["max"] = self.max()

        elif self.dtype == Boolean:
            stats_dtype = Int64
            stats = {
                "count": self.count(),
                "null_count": self.null_count(),
                "sum": self.sum(),
            }
        elif self.dtype == String:
            stats_dtype = Int64
            stats = {
                "count": self.count(),
                "null_count": self.null_count(),
                "unique": self.n_unique(),
            }
        elif self.dtype.is_temporal():
            # we coerce all to string, because a polars column
            # only has a single dtype and dates: datetime and count: int don't match
            stats_dtype = String
            stats = {
                "count": str(self.count()),
                "null_count": str(self.null_count()),
                "min": str(self.dt.min()),
                "50%": str(self.dt.median()),
                "max": str(self.dt.max()),
            }
        else:
            raise TypeError(f"cannot describe Series of data type {self.dtype}")

        return pl.DataFrame(
            {"statistic": stats.keys(), "value": stats.values()},
            schema={"statistic": String, "value": stats_dtype},
        )
