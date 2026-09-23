    def join_asof(
        self,
        other: DataFrame,
        *,
        left_on: str | None | Expr = None,
        right_on: str | None | Expr = None,
        on: str | None | Expr = None,
        by_left: str | Sequence[str] | None = None,
        by_right: str | Sequence[str] | None = None,
        by: str | Sequence[str] | None = None,
        strategy: AsofJoinStrategy = "backward",
        suffix: str = "_right",
        tolerance: str | int | float | timedelta | None = None,
        allow_parallel: bool = True,
        force_parallel: bool = False,
        coalesce: bool | None = None,
    ) -> DataFrame:
        """
        Perform an asof join.

        This is similar to a left-join except that we match on nearest key rather than
        equal keys.

        Both DataFrames must be sorted by the asof_join key.

        For each row in the left DataFrame:

          - A "backward" search selects the last row in the right DataFrame whose
            'on' key is less than or equal to the left's key.

          - A "forward" search selects the first row in the right DataFrame whose
            'on' key is greater than or equal to the left's key.

          - A "nearest" search selects the last row in the right DataFrame whose value
            is nearest to the left's key. String keys are not currently supported for a
            nearest search.

        The default is "backward".

        Parameters
        ----------
        other
            Lazy DataFrame to join with.
        left_on
            Join column of the left DataFrame.
        right_on
            Join column of the right DataFrame.
        on
            Join column of both DataFrames. If set, `left_on` and `right_on` should be
            None.
        by
            join on these columns before doing asof join
        by_left
            join on these columns before doing asof join
        by_right
            join on these columns before doing asof join
        strategy : {'backward', 'forward', 'nearest'}
            Join strategy.
        suffix
            Suffix to append to columns with a duplicate name.
        tolerance
            Numeric tolerance. By setting this the join will only be done if the near
            keys are within this distance. If an asof join is done on columns of dtype
            "Date", "Datetime", "Duration" or "Time", use either a datetime.timedelta
            object or the following string language:

                - 1ns   (1 nanosecond)
                - 1us   (1 microsecond)
                - 1ms   (1 millisecond)
                - 1s    (1 second)
                - 1m    (1 minute)
                - 1h    (1 hour)
                - 1d    (1 calendar day)
                - 1w    (1 calendar week)
                - 1mo   (1 calendar month)
                - 1q    (1 calendar quarter)
                - 1y    (1 calendar year)

                Or combine them:
                "3d12h4m25s" # 3 days, 12 hours, 4 minutes, and 25 seconds

                By "calendar day", we mean the corresponding time on the next day
                (which may not be 24 hours, due to daylight savings). Similarly for
                "calendar week", "calendar month", "calendar quarter", and
                "calendar year".

        allow_parallel
            Allow the physical plan to optionally evaluate the computation of both
            DataFrames up to the join in parallel.
        force_parallel
            Force the physical plan to evaluate the computation of both DataFrames up to
            the join in parallel.
        coalesce
            Coalescing behavior (merging of join columns).

            - None: -> join specific.
            - True: -> Always coalesce join columns.
            - False: -> Never coalesce join columns.

            Note that joining on any other expressions than `col`
            will turn off coalescing.

        Examples
        --------
        >>> from datetime import date
        >>> gdp = pl.DataFrame(
        ...     {
        ...         "date": pl.date_range(
        ...             date(2016, 1, 1),
        ...             date(2020, 1, 1),
        ...             "1y",
        ...             eager=True,
        ...         ),
        ...         "gdp": [4164, 4411, 4566, 4696, 4827],
        ...     }
        ... )
        >>> gdp
        shape: (5, 2)
        ┌────────────┬──────┐
        │ date       ┆ gdp  │
        │ ---        ┆ ---  │
        │ date       ┆ i64  │
        ╞════════════╪══════╡
        │ 2016-01-01 ┆ 4164 │
        │ 2017-01-01 ┆ 4411 │
        │ 2018-01-01 ┆ 4566 │
        │ 2019-01-01 ┆ 4696 │
        │ 2020-01-01 ┆ 4827 │
        └────────────┴──────┘

        >>> population = pl.DataFrame(
        ...     {
        ...         "date": [date(2016, 3, 1), date(2018, 8, 1), date(2019, 1, 1)],
        ...         "population": [82.19, 82.66, 83.12],
        ...     }
        ... ).sort("date")
        >>> population
        shape: (3, 2)
        ┌────────────┬────────────┐
        │ date       ┆ population │
        │ ---        ┆ ---        │
        │ date       ┆ f64        │
        ╞════════════╪════════════╡
        │ 2016-03-01 ┆ 82.19      │
        │ 2018-08-01 ┆ 82.66      │
        │ 2019-01-01 ┆ 83.12      │
        └────────────┴────────────┘

        Note how the dates don't quite match. If we join them using `join_asof` and
        `strategy='backward'`, then each date from `population` which doesn't have an
        exact match is matched with the closest earlier date from `gdp`:

        >>> population.join_asof(gdp, on="date", strategy="backward")
        shape: (3, 3)
        ┌────────────┬────────────┬──────┐
        │ date       ┆ population ┆ gdp  │
        │ ---        ┆ ---        ┆ ---  │
        │ date       ┆ f64        ┆ i64  │
        ╞════════════╪════════════╪══════╡
        │ 2016-03-01 ┆ 82.19      ┆ 4164 │
        │ 2018-08-01 ┆ 82.66      ┆ 4566 │
        │ 2019-01-01 ┆ 83.12      ┆ 4696 │
        └────────────┴────────────┴──────┘

        Note how:

        - date `2016-03-01` from `population` is matched with `2016-01-01` from `gdp`;
        - date `2018-08-01` from `population` is matched with `2018-01-01` from `gdp`.

        If we instead use `strategy='forward'`, then each date from `population` which
        doesn't have an exact match is matched with the closest later date from `gdp`:

        >>> population.join_asof(gdp, on="date", strategy="forward")
        shape: (3, 3)
        ┌────────────┬────────────┬──────┐
        │ date       ┆ population ┆ gdp  │
        │ ---        ┆ ---        ┆ ---  │
        │ date       ┆ f64        ┆ i64  │
        ╞════════════╪════════════╪══════╡
        │ 2016-03-01 ┆ 82.19      ┆ 4411 │
        │ 2018-08-01 ┆ 82.66      ┆ 4696 │
        │ 2019-01-01 ┆ 83.12      ┆ 4696 │
        └────────────┴────────────┴──────┘

        Note how:

        - date `2016-03-01` from `population` is matched with `2017-01-01` from `gdp`;
        - date `2018-08-01` from `population` is matched with `2019-01-01` from `gdp`.

        Finally, `strategy='nearest'` gives us a mix of the two results above, as each
        date from `population` which doesn't have an exact match is matched with the
        closest date from `gdp`, regardless of whether it's earlier or later:

        >>> population.join_asof(gdp, on="date", strategy="nearest")
        shape: (3, 3)
        ┌────────────┬────────────┬──────┐
        │ date       ┆ population ┆ gdp  │
        │ ---        ┆ ---        ┆ ---  │
        │ date       ┆ f64        ┆ i64  │
        ╞════════════╪════════════╪══════╡
        │ 2016-03-01 ┆ 82.19      ┆ 4164 │
        │ 2018-08-01 ┆ 82.66      ┆ 4696 │
        │ 2019-01-01 ┆ 83.12      ┆ 4696 │
        └────────────┴────────────┴──────┘

        Note how:

        - date `2016-03-01` from `population` is matched with `2016-01-01` from `gdp`;
        - date `2018-08-01` from `population` is matched with `2019-01-01` from `gdp`.

        They `by` argument allows joining on another column first, before the asof join.
        In this example we join by `country` first, then asof join by date, as above.

        >>> gdp_dates = pl.date_range(  # fmt: skip
        ...     date(2016, 1, 1), date(2020, 1, 1), "1y", eager=True
        ... )
        >>> gdp2 = pl.DataFrame(
        ...     {
        ...         "country": ["Germany"] * 5 + ["Netherlands"] * 5,
        ...         "date": pl.concat([gdp_dates, gdp_dates]),
        ...         "gdp": [4164, 4411, 4566, 4696, 4827, 784, 833, 914, 910, 909],
        ...     }
        ... ).sort("country", "date")
        >>>
        >>> gdp2
        shape: (10, 3)
        ┌─────────────┬────────────┬──────┐
        │ country     ┆ date       ┆ gdp  │
        │ ---         ┆ ---        ┆ ---  │
        │ str         ┆ date       ┆ i64  │
        ╞═════════════╪════════════╪══════╡
        │ Germany     ┆ 2016-01-01 ┆ 4164 │
        │ Germany     ┆ 2017-01-01 ┆ 4411 │
        │ Germany     ┆ 2018-01-01 ┆ 4566 │
        │ Germany     ┆ 2019-01-01 ┆ 4696 │
        │ Germany     ┆ 2020-01-01 ┆ 4827 │
        │ Netherlands ┆ 2016-01-01 ┆ 784  │
        │ Netherlands ┆ 2017-01-01 ┆ 833  │
        │ Netherlands ┆ 2018-01-01 ┆ 914  │
        │ Netherlands ┆ 2019-01-01 ┆ 910  │
        │ Netherlands ┆ 2020-01-01 ┆ 909  │
        └─────────────┴────────────┴──────┘
        >>> pop2 = pl.DataFrame(
        ...     {
        ...         "country": ["Germany"] * 3 + ["Netherlands"] * 3,
        ...         "date": [
        ...             date(2016, 3, 1),
        ...             date(2018, 8, 1),
        ...             date(2019, 1, 1),
        ...             date(2016, 3, 1),
        ...             date(2018, 8, 1),
        ...             date(2019, 1, 1),
        ...         ],
        ...         "population": [82.19, 82.66, 83.12, 17.11, 17.32, 17.40],
        ...     }
        ... ).sort("country", "date")
        >>>
        >>> pop2
        shape: (6, 3)
        ┌─────────────┬────────────┬────────────┐
        │ country     ┆ date       ┆ population │
        │ ---         ┆ ---        ┆ ---        │
        │ str         ┆ date       ┆ f64        │
        ╞═════════════╪════════════╪════════════╡
        │ Germany     ┆ 2016-03-01 ┆ 82.19      │
        │ Germany     ┆ 2018-08-01 ┆ 82.66      │
        │ Germany     ┆ 2019-01-01 ┆ 83.12      │
        │ Netherlands ┆ 2016-03-01 ┆ 17.11      │
        │ Netherlands ┆ 2018-08-01 ┆ 17.32      │
        │ Netherlands ┆ 2019-01-01 ┆ 17.4       │
        └─────────────┴────────────┴────────────┘
        >>> pop2.join_asof(gdp2, by="country", on="date", strategy="nearest")
        shape: (6, 4)
        ┌─────────────┬────────────┬────────────┬──────┐
        │ country     ┆ date       ┆ population ┆ gdp  │
        │ ---         ┆ ---        ┆ ---        ┆ ---  │
        │ str         ┆ date       ┆ f64        ┆ i64  │
        ╞═════════════╪════════════╪════════════╪══════╡
        │ Germany     ┆ 2016-03-01 ┆ 82.19      ┆ 4164 │
        │ Germany     ┆ 2018-08-01 ┆ 82.66      ┆ 4696 │
        │ Germany     ┆ 2019-01-01 ┆ 83.12      ┆ 4696 │
        │ Netherlands ┆ 2016-03-01 ┆ 17.11      ┆ 784  │
        │ Netherlands ┆ 2018-08-01 ┆ 17.32      ┆ 910  │
        │ Netherlands ┆ 2019-01-01 ┆ 17.4       ┆ 910  │
        └─────────────┴────────────┴────────────┴──────┘

        """
        if not isinstance(other, DataFrame):
            msg = f"expected `other` join table to be a DataFrame, got {type(other).__name__!r}"
            raise TypeError(msg)

        if on is not None:
            if not isinstance(on, (str, pl.Expr)):
                msg = f"expected `on` to be str or Expr, got {type(on).__name__!r}"
                raise TypeError(msg)
        else:
            if not isinstance(left_on, (str, pl.Expr)):
                msg = f"expected `left_on` to be str or Expr, got {type(left_on).__name__!r}"
                raise TypeError(msg)
            elif not isinstance(right_on, (str, pl.Expr)):
                msg = f"expected `right_on` to be str or Expr, got {type(right_on).__name__!r}"
                raise TypeError(msg)

        return (
            self.lazy()
            .join_asof(
                other.lazy(),
                left_on=left_on,
                right_on=right_on,
                on=on,
                by_left=by_left,
                by_right=by_right,
                by=by,
                strategy=strategy,
                suffix=suffix,
                tolerance=tolerance,
                allow_parallel=allow_parallel,
                force_parallel=force_parallel,
                coalesce=coalesce,
            )
            .collect(_eager=True)
        )
