    def dst_offset(self) -> Expr:
        """
        Additional offset currently in effect (typically due to daylight saving time).

        Returns
        -------
        Expr
            Expression of data type :class:`Duration`.

        See Also
        --------
        Expr.dt.base_utc_offset : Base offset from UTC.

        Examples
        --------
        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "ts": [datetime(2020, 10, 25), datetime(2020, 10, 26)],
        ...     }
        ... )
        >>> df = df.with_columns(pl.col("ts").dt.replace_time_zone("Europe/London"))
        >>> df.with_columns(pl.col("ts").dt.dst_offset().alias("dst_offset"))
        shape: (2, 2)
        ┌─────────────────────────────┬──────────────┐
        │ ts                          ┆ dst_offset   │
        │ ---                         ┆ ---          │
        │ datetime[μs, Europe/London] ┆ duration[ms] │
        ╞═════════════════════════════╪══════════════╡
        │ 2020-10-25 00:00:00 BST     ┆ 1h           │
        │ 2020-10-26 00:00:00 GMT     ┆ 0ms          │
        └─────────────────────────────┴──────────────┘
        """
        return wrap_expr(self._pyexpr.dt_dst_offset())
