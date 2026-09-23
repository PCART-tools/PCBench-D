    def add_business_days(
        self,
        n: int | IntoExpr,
        week_mask: Iterable[bool] = (True, True, True, True, True, False, False),
        holidays: Iterable[dt.date] = (),
        roll: Roll = "raise",
    ) -> Expr:
        """
        Offset by `n` business days.

        Parameters
        ----------
        n
            Number of business days to offset by. Can be a single number of an
            expression.
        week_mask
            Which days of the week to count. The default is Monday to Friday.
            If you wanted to count only Monday to Thursday, you would pass
            `(True, True, True, True, False, False, False)`.
        holidays
            Holidays to exclude from the count. The Python package
            `python-holidays <https://github.com/vacanza/python-holidays>`_
            may come in handy here. You can install it with ``pip install holidays``,
            and then, to get all Dutch holidays for years 2020-2024:

            .. code-block:: python

                import holidays

                my_holidays = holidays.country_holidays("NL", years=range(2020, 2025))

            and pass `holidays=my_holidays` when you call `business_day_count`.
        roll
            What to do when the start date lands on a non-business day. Options are:

            - `'raise'`: raise an error
            - `'forward'`: move to the next business day
            - `'backward'`: move to the previous business day

        Returns
        -------
        Expr
            Data type is preserved.

        Examples
        --------
        >>> from datetime import date
        >>> df = pl.DataFrame({"start": [date(2020, 1, 1), date(2020, 1, 2)]})
        >>> df.with_columns(result=pl.col("start").dt.add_business_days(5))
        shape: (2, 2)
        ┌────────────┬────────────┐
        │ start      ┆ result     │
        │ ---        ┆ ---        │
        │ date       ┆ date       │
        ╞════════════╪════════════╡
        │ 2020-01-01 ┆ 2020-01-08 │
        │ 2020-01-02 ┆ 2020-01-09 │
        └────────────┴────────────┘

        You can pass a custom weekend - for example, if you only take Sunday off:

        >>> week_mask = (True, True, True, True, True, True, False)
        >>> df.with_columns(result=pl.col("start").dt.add_business_days(5, week_mask))
        shape: (2, 2)
        ┌────────────┬────────────┐
        │ start      ┆ result     │
        │ ---        ┆ ---        │
        │ date       ┆ date       │
        ╞════════════╪════════════╡
        │ 2020-01-01 ┆ 2020-01-07 │
        │ 2020-01-02 ┆ 2020-01-08 │
        └────────────┴────────────┘

        You can also pass a list of holidays:

        >>> from datetime import date
        >>> holidays = [date(2020, 1, 3), date(2020, 1, 6)]
        >>> df.with_columns(
        ...     result=pl.col("start").dt.add_business_days(5, holidays=holidays)
        ... )
        shape: (2, 2)
        ┌────────────┬────────────┐
        │ start      ┆ result     │
        │ ---        ┆ ---        │
        │ date       ┆ date       │
        ╞════════════╪════════════╡
        │ 2020-01-01 ┆ 2020-01-10 │
        │ 2020-01-02 ┆ 2020-01-13 │
        └────────────┴────────────┘

        Roll all dates forwards to the next business day:

        >>> df = pl.DataFrame({"start": [date(2020, 1, 5), date(2020, 1, 6)]})
        >>> df.with_columns(
        ...     rolled_forwards=pl.col("start").dt.add_business_days(0, roll="forward")
        ... )
        shape: (2, 2)
        ┌────────────┬─────────────────┐
        │ start      ┆ rolled_forwards │
        │ ---        ┆ ---             │
        │ date       ┆ date            │
        ╞════════════╪═════════════════╡
        │ 2020-01-05 ┆ 2020-01-06      │
        │ 2020-01-06 ┆ 2020-01-06      │
        └────────────┴─────────────────┘
        """
        n_pyexpr = parse_as_expression(n)
        unix_epoch = dt.date(1970, 1, 1)
        return wrap_expr(
            self._pyexpr.dt_add_business_days(
                n_pyexpr,
                week_mask,
                [(holiday - unix_epoch).days for holiday in holidays],
                roll,
            )
        )
