    def to_string(self, format: str) -> Expr:
        """
        Convert a Date/Time/Datetime column into a Utf8 column with the given format.

        Similar to ``cast(pl.Utf8)``, but this method allows you to customize the
        formatting of the resulting string.

        Parameters
        ----------
        format
            Format to use, refer to the `chrono strftime documentation
            <https://docs.rs/chrono/latest/chrono/format/strftime/index.html>`_
            for specification. Example: ``"%y-%m-%d"``.

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
        ...     .dt.to_string("%Y/%m/%d %H:%M:%S")
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

        """
        return wrap_expr(self._pyexpr.dt_to_string(format))
