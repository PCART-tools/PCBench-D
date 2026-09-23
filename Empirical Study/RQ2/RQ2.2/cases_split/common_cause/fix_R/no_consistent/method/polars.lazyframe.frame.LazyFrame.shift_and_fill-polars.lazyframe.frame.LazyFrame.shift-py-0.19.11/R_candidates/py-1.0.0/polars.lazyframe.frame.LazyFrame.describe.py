    def describe(
        self,
        percentiles: Sequence[float] | float | None = (0.25, 0.50, 0.75),
        *,
        interpolation: RollingInterpolationMethod = "nearest",
    ) -> DataFrame:
        """
        Creates a summary of statistics for a LazyFrame, returning a DataFrame.

        Parameters
        ----------
        percentiles
            One or more percentiles to include in the summary statistics.
            All values must be in the range `[0, 1]`.

        interpolation : {'nearest', 'higher', 'lower', 'midpoint', 'linear'}
            Interpolation method used when calculating percentiles.

        Returns
        -------
        DataFrame

        Notes
        -----
        The median is included by default as the 50% percentile.

        Warnings
        --------
        * This method does *not* maintain the laziness of the frame, and will `collect`
          the final result. This could potentially be an expensive operation.
        * We do not guarantee the output of `describe` to be stable. It will show
          statistics that we deem informative, and may be updated in the future.
          Using `describe` programmatically (versus interactive exploration) is
          not recommended for this reason.

        Examples
        --------
        >>> from datetime import date, time
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "float": [1.0, 2.8, 3.0],
        ...         "int": [40, 50, None],
        ...         "bool": [True, False, True],
        ...         "str": ["zz", "xx", "yy"],
        ...         "date": [date(2020, 1, 1), date(2021, 7, 5), date(2022, 12, 31)],
        ...         "time": [time(10, 20, 30), time(14, 45, 50), time(23, 15, 10)],
        ...     }
        ... )

        Show default frame statistics:

        >>> lf.describe()
        shape: (9, 7)
        ┌────────────┬──────────┬──────────┬──────────┬──────┬─────────────────────┬──────────┐
        │ statistic  ┆ float    ┆ int      ┆ bool     ┆ str  ┆ date                ┆ time     │
        │ ---        ┆ ---      ┆ ---      ┆ ---      ┆ ---  ┆ ---                 ┆ ---      │
        │ str        ┆ f64      ┆ f64      ┆ f64      ┆ str  ┆ str                 ┆ str      │
        ╞════════════╪══════════╪══════════╪══════════╪══════╪═════════════════════╪══════════╡
        │ count      ┆ 3.0      ┆ 2.0      ┆ 3.0      ┆ 3    ┆ 3                   ┆ 3        │
        │ null_count ┆ 0.0      ┆ 1.0      ┆ 0.0      ┆ 0    ┆ 0                   ┆ 0        │
        │ mean       ┆ 2.266667 ┆ 45.0     ┆ 0.666667 ┆ null ┆ 2021-07-02 16:00:00 ┆ 16:07:10 │
        │ std        ┆ 1.101514 ┆ 7.071068 ┆ null     ┆ null ┆ null                ┆ null     │
        │ min        ┆ 1.0      ┆ 40.0     ┆ 0.0      ┆ xx   ┆ 2020-01-01          ┆ 10:20:30 │
        │ 25%        ┆ 2.8      ┆ 40.0     ┆ null     ┆ null ┆ 2021-07-05          ┆ 14:45:50 │
        │ 50%        ┆ 2.8      ┆ 50.0     ┆ null     ┆ null ┆ 2021-07-05          ┆ 14:45:50 │
        │ 75%        ┆ 3.0      ┆ 50.0     ┆ null     ┆ null ┆ 2022-12-31          ┆ 23:15:10 │
        │ max        ┆ 3.0      ┆ 50.0     ┆ 1.0      ┆ zz   ┆ 2022-12-31          ┆ 23:15:10 │
        └────────────┴──────────┴──────────┴──────────┴──────┴─────────────────────┴──────────┘

        Customize which percentiles are displayed, applying linear interpolation:

        >>> with pl.Config(tbl_rows=12):
        ...     lf.describe(
        ...         percentiles=[0.1, 0.3, 0.5, 0.7, 0.9],
        ...         interpolation="linear",
        ...     )
        shape: (11, 7)
        ┌────────────┬──────────┬──────────┬──────────┬──────┬─────────────────────┬──────────┐
        │ statistic  ┆ float    ┆ int      ┆ bool     ┆ str  ┆ date                ┆ time     │
        │ ---        ┆ ---      ┆ ---      ┆ ---      ┆ ---  ┆ ---                 ┆ ---      │
        │ str        ┆ f64      ┆ f64      ┆ f64      ┆ str  ┆ str                 ┆ str      │
        ╞════════════╪══════════╪══════════╪══════════╪══════╪═════════════════════╪══════════╡
        │ count      ┆ 3.0      ┆ 2.0      ┆ 3.0      ┆ 3    ┆ 3                   ┆ 3        │
        │ null_count ┆ 0.0      ┆ 1.0      ┆ 0.0      ┆ 0    ┆ 0                   ┆ 0        │
        │ mean       ┆ 2.266667 ┆ 45.0     ┆ 0.666667 ┆ null ┆ 2021-07-02 16:00:00 ┆ 16:07:10 │
        │ std        ┆ 1.101514 ┆ 7.071068 ┆ null     ┆ null ┆ null                ┆ null     │
        │ min        ┆ 1.0      ┆ 40.0     ┆ 0.0      ┆ xx   ┆ 2020-01-01          ┆ 10:20:30 │
        │ 10%        ┆ 1.36     ┆ 41.0     ┆ null     ┆ null ┆ 2020-04-20          ┆ 11:13:34 │
        │ 30%        ┆ 2.08     ┆ 43.0     ┆ null     ┆ null ┆ 2020-11-26          ┆ 12:59:42 │
        │ 50%        ┆ 2.8      ┆ 45.0     ┆ null     ┆ null ┆ 2021-07-05          ┆ 14:45:50 │
        │ 70%        ┆ 2.88     ┆ 47.0     ┆ null     ┆ null ┆ 2022-02-07          ┆ 18:09:34 │
        │ 90%        ┆ 2.96     ┆ 49.0     ┆ null     ┆ null ┆ 2022-09-13          ┆ 21:33:18 │
        │ max        ┆ 3.0      ┆ 50.0     ┆ 1.0      ┆ zz   ┆ 2022-12-31          ┆ 23:15:10 │
        └────────────┴──────────┴──────────┴──────────┴──────┴─────────────────────┴──────────┘
        """  # noqa: W505
        from polars.convert import from_dict

        schema = self.collect_schema()

        if not schema:
            msg = "cannot describe a LazyFrame that has no columns"
            raise TypeError(msg)

        # create list of metrics
        metrics = ["count", "null_count", "mean", "std", "min"]
        if quantiles := parse_percentiles(percentiles):
            metrics.extend(f"{q * 100:g}%" for q in quantiles)
        metrics.append("max")

        @lru_cache
        def skip_minmax(dt: PolarsDataType) -> bool:
            return dt.is_nested() or dt in (Categorical, Enum, Null, Object, Unknown)

        # determine which columns will produce std/mean/percentile/etc
        # statistics in a single pass over the frame schema
        has_numeric_result, sort_cols = set(), set()
        metric_exprs: list[Expr] = []
        null = F.lit(None)

        for c, dtype in schema.items():
            is_numeric = dtype.is_numeric()
            is_temporal = not is_numeric and dtype.is_temporal()

            # counts
            count_exprs = [
                F.col(c).count().name.prefix("count:"),
                F.col(c).null_count().name.prefix("null_count:"),
            ]
            # mean
            mean_expr = (
                F.col(c).mean()
                if is_temporal or is_numeric or dtype == Boolean
                else null
            )

            # standard deviation, min, max
            expr_std = F.col(c).std() if is_numeric else null
            min_expr = F.col(c).min() if not skip_minmax(dtype) else null
            max_expr = F.col(c).max() if not skip_minmax(dtype) else null

            # percentiles
            pct_exprs = []
            for p in quantiles:
                if is_numeric or is_temporal:
                    pct_expr = (
                        F.col(c).to_physical().quantile(p, interpolation).cast(dtype)
                        if is_temporal
                        else F.col(c).quantile(p, interpolation)
                    )
                    sort_cols.add(c)
                else:
                    pct_expr = null
                pct_exprs.append(pct_expr.alias(f"{p}:{c}"))

            if is_numeric or dtype.is_nested() or dtype in (Null, Boolean):
                has_numeric_result.add(c)

            # add column expressions (in end-state 'metrics' list order)
            metric_exprs.extend(
                [
                    *count_exprs,
                    mean_expr.alias(f"mean:{c}"),
                    expr_std.alias(f"std:{c}"),
                    min_expr.alias(f"min:{c}"),
                    *pct_exprs,
                    max_expr.alias(f"max:{c}"),
                ]
            )

        # calculate requested metrics in parallel, then collect the result
        df_metrics = (
            (
                # if more than one quantile, sort the relevant columns to make them O(1)
                # TODO: drop sort once we have efficient retrieval of multiple quantiles
                self.with_columns(F.col(c).sort() for c in sort_cols)
                if sort_cols
                else self
            )
            .select(*metric_exprs)
            .collect()
        )

        # reshape wide result
        n_metrics = len(metrics)
        column_metrics = [
            df_metrics.row(0)[(n * n_metrics) : (n + 1) * n_metrics]
            for n in range(schema.len())
        ]
        summary = dict(zip(schema, column_metrics))

        # cast by column type (numeric/bool -> float), (other -> string)
        for c in schema:
            summary[c] = [  # type: ignore[assignment]
                (
                    None
                    if (v is None or isinstance(v, dict))
                    else (float(v) if (c in has_numeric_result) else str(v))
                )
                for v in summary[c]
            ]

        # return results as a DataFrame
        df_summary = from_dict(summary)
        df_summary.insert_column(0, pl.Series("statistic", metrics))
        return df_summary
