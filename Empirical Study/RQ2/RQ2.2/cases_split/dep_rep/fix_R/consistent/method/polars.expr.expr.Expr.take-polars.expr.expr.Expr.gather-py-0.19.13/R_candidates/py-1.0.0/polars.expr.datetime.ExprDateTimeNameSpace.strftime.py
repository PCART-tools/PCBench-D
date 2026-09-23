    def strftime(self, format: str) -> Expr:
        """
        Convert a Date/Time/Datetime column into a String column with the given format.

        Similar to `cast(pl.String)`, but this method allows you to customize the
        formatting of the resulting string.

        Alias for :func:`to_string`.

        Parameters
        ----------
        format
            Format to use, refer to the `chrono strftime documentation
            <https://docs.rs/chrono/latest/chrono/format/strftime/index.html>`_
            for specification. Example: `"%y-%m-%d"`.

        See Also
        --------
        to_string : The identical expression for which `strftime` is an alias.

        Examples
        --------
        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "datetime": [
        ...             datetime(2020, 3, 1),
        ...             datetime(2020, 4, 1),
        ...             datetime(2020, 5, 1),
        ...         ]
        ...     }
        ... )
        >>> df.with_columns(
        ...     pl.col("datetime")
        ...     .dt.strftime("%Y/%m/%d %H:%M:%S")
        ...     .alias("datetime_string")
        ... )
        shape: (3, 2)
        ┌─────────────────────┬─────────────────────┐
        │ datetime            ┆ datetime_string     │
        │ ---                 ┆ ---                 │
        │ datetime[μs]        ┆ str                 │
        ╞═════════════════════╪═════════════════════╡
        │ 2020-03-01 00:00:00 ┆ 2020/03/01 00:00:00 │
        │ 2020-04-01 00:00:00 ┆ 2020/04/01 00:00:00 │
        │ 2020-05-01 00:00:00 ┆ 2020/05/01 00:00:00 │
        └─────────────────────┴─────────────────────┘

        If you're interested in the day name / month name, you can use
        `'%A'` / `'%B'`:

        >>> df.with_columns(
        ...     day_name=pl.col("datetime").dt.strftime("%A"),
        ...     month_name=pl.col("datetime").dt.strftime("%B"),
        ... )
        shape: (3, 3)
        ┌─────────────────────┬───────────┬────────────┐
        │ datetime            ┆ day_name  ┆ month_name │
        │ ---                 ┆ ---       ┆ ---        │
        │ datetime[μs]        ┆ str       ┆ str        │
        ╞═════════════════════╪═══════════╪════════════╡
        │ 2020-03-01 00:00:00 ┆ Sunday    ┆ March      │
        │ 2020-04-01 00:00:00 ┆ Wednesday ┆ April      │
        │ 2020-05-01 00:00:00 ┆ Friday    ┆ May        │
        └─────────────────────┴───────────┴────────────┘
        """
        return self.to_string(format)
