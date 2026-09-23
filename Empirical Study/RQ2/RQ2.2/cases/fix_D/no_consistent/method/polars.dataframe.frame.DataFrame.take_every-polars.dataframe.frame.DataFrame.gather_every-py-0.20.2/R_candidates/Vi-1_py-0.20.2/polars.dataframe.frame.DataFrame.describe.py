    def describe(
        self, percentiles: Sequence[float] | float | None = (0.25, 0.50, 0.75)
    ) -> Self:
        """
        Summary statistics for a DataFrame.

        Parameters
        ----------
        percentiles
            One or more percentiles to include in the summary statistics.
            All values must be in the range `[0, 1]`.

        Notes
        -----
        The median is included by default as the 50% percentile.

        Warnings
        --------
        We will never guarantee the output of describe to be stable.
        It will show statistics that we deem informative and may
        be updated in the future.

        See Also
        --------
        glimpse

        Examples
        --------
        >>> from datetime import date
        >>> df = pl.DataFrame(
        ...     {
        ...         "float": [1.0, 2.8, 3.0],
        ...         "int": [4, 5, None],
        ...         "bool": [True, False, True],
        ...         "str": [None, "b", "c"],
        ...         "str2": ["usd", "eur", None],
        ...         "date": [date(2020, 1, 1), date(2021, 1, 1), date(2022, 1, 1)],
        ...     }
        ... )
        >>> df.describe()
        shape: (9, 7)
        ┌────────────┬──────────┬──────────┬───────┬──────┬──────┬────────────┐
        │ describe   ┆ float    ┆ int      ┆ bool  ┆ str  ┆ str2 ┆ date       │
        │ ---        ┆ ---      ┆ ---      ┆ ---   ┆ ---  ┆ ---  ┆ ---        │
        │ str        ┆ f64      ┆ f64      ┆ str   ┆ str  ┆ str  ┆ str        │
        ╞════════════╪══════════╪══════════╪═══════╪══════╪══════╪════════════╡
        │ count      ┆ 3.0      ┆ 2.0      ┆ 3     ┆ 2    ┆ 2    ┆ 3          │
        │ null_count ┆ 0.0      ┆ 1.0      ┆ 0     ┆ 1    ┆ 1    ┆ 0          │
        │ mean       ┆ 2.266667 ┆ 4.5      ┆ null  ┆ null ┆ null ┆ null       │
        │ std        ┆ 1.101514 ┆ 0.707107 ┆ null  ┆ null ┆ null ┆ null       │
        │ min        ┆ 1.0      ┆ 4.0      ┆ False ┆ b    ┆ eur  ┆ 2020-01-01 │
        │ 25%        ┆ 2.8      ┆ 4.0      ┆ null  ┆ null ┆ null ┆ null       │
        │ 50%        ┆ 2.8      ┆ 5.0      ┆ null  ┆ null ┆ null ┆ null       │
        │ 75%        ┆ 3.0      ┆ 5.0      ┆ null  ┆ null ┆ null ┆ null       │
        │ max        ┆ 3.0      ┆ 5.0      ┆ True  ┆ c    ┆ usd  ┆ 2022-01-01 │
        └────────────┴──────────┴──────────┴───────┴──────┴──────┴────────────┘

        """
        if not self.columns:
            raise TypeError("cannot describe a DataFrame without any columns")

        # Determine which columns should get std/mean/percentile statistics
        stat_cols = {c for c, dt in self.schema.items() if dt.is_numeric()}

        # Determine metrics and optional/additional percentiles
        metrics = ["count", "null_count", "mean", "std", "min"]
        percentile_exprs = []
        for p in parse_percentiles(percentiles):
            for c in self.columns:
                expr = F.col(c).quantile(p) if c in stat_cols else F.lit(None)
                expr = expr.alias(f"{p}:{c}")
                percentile_exprs.append(expr)
            metrics.append(f"{p:.0%}")
        metrics.append("max")

        mean_exprs = [
            (F.col(c).mean() if c in stat_cols else F.lit(None)).alias(f"mean:{c}")
            for c in self.columns
        ]
        std_exprs = [
            (F.col(c).std() if c in stat_cols else F.lit(None)).alias(f"std:{c}")
            for c in self.columns
        ]

        minmax_cols = {
            c
            for c, dt in self.schema.items()
            if not dt.is_nested()
            and dt not in (Object, Null, Unknown, Categorical, Enum)
        }
        min_exprs = [
            (F.col(c).min() if c in minmax_cols else F.lit(None)).alias(f"min:{c}")
            for c in self.columns
        ]
        max_exprs = [
            (F.col(c).max() if c in minmax_cols else F.lit(None)).alias(f"max:{c}")
            for c in self.columns
        ]

        # Calculate metrics in parallel
        df_metrics = self.select(
            F.all().count().name.prefix("count:"),
            F.all().null_count().name.prefix("null_count:"),
            *mean_exprs,
            *std_exprs,
            *min_exprs,
            *percentile_exprs,
            *max_exprs,
        )

        # Reshape wide result
        described = [
            df_metrics.row(0)[(n * self.width) : (n + 1) * self.width]
            for n in range(len(metrics))
        ]

        # Cast by column type (numeric/bool -> float), (other -> string)
        summary = dict(zip(self.columns, list(zip(*described))))
        for c in self.columns:
            summary[c] = [  # type: ignore[assignment]
                None
                if (v is None or isinstance(v, dict))
                else (float(v) if c in stat_cols else str(v))
                for v in summary[c]
            ]

        # Return results as a DataFrame
        df_summary = self._from_dict(summary)
        df_summary.insert_column(0, pl.Series("describe", metrics))
        return df_summary
