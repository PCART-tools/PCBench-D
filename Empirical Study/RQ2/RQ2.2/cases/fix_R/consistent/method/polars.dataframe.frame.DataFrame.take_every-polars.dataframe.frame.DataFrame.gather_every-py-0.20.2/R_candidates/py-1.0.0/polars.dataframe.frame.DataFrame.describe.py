    def describe(
        self,
        percentiles: Sequence[float] | float | None = (0.25, 0.50, 0.75),
        *,
        interpolation: RollingInterpolationMethod = "nearest",
    ) -> DataFrame:
        """
        Summary statistics for a DataFrame.

        Parameters
        ----------
        percentiles
            One or more percentiles to include in the summary statistics.
            All values must be in the range `[0, 1]`.

        interpolation : {'nearest', 'higher', 'lower', 'midpoint', 'linear'}
            Interpolation method used when calculating percentiles.

        Notes
        -----
        The median is included by default as the 50% percentile.

        Warnings
        --------
        We do not guarantee the output of `describe` to be stable. It will show
        statistics that we deem informative, and may be updated in the future.
        Using `describe` programmatically (versus interactive exploration) is
        not recommended for this reason.

        See Also
        --------
        glimpse

        Examples
        --------
        >>> from datetime import date, time
        >>> df = pl.DataFrame(
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

        >>> df.describe()
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
        ...     df.describe(
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
        if not self.columns:
            msg = "cannot describe a DataFrame that has no columns"
            raise TypeError(msg)

        return self.lazy().describe(
            percentiles=percentiles, interpolation=interpolation
        )
