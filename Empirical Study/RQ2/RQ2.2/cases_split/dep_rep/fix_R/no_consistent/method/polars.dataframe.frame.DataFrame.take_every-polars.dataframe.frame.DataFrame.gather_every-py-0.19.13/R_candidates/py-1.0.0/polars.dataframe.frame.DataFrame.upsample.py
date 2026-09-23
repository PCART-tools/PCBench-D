    @deprecate_renamed_parameter("by", "group_by", version="0.20.14")
    def upsample(
        self,
        time_column: str,
        *,
        every: str | timedelta,
        group_by: str | Sequence[str] | None = None,
        maintain_order: bool = False,
    ) -> DataFrame:
        """
        Upsample a DataFrame at a regular frequency.

        The `every` argument is created with the following string language:

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
        - 1i    (1 index count)

        Or combine them:

        - "3d12h4m25s" # 3 days, 12 hours, 4 minutes, and 25 seconds


        By "calendar day", we mean the corresponding time on the next day (which may
        not be 24 hours, due to daylight savings). Similarly for "calendar week",
        "calendar month", "calendar quarter", and "calendar year".

        Parameters
        ----------
        time_column
            Time column will be used to determine a date_range.
            Note that this column has to be sorted for the output to make sense.
        every
            Interval will start 'every' duration.
        group_by
            First group by these columns and then upsample for every group.
        maintain_order
            Keep the ordering predictable. This is slower.

        Returns
        -------
        DataFrame
            Result will be sorted by `time_column` (but note that if `group_by` columns
            are passed, it will only be sorted within each group).

        Examples
        --------
        Upsample a DataFrame by a certain interval.

        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "time": [
        ...             datetime(2021, 2, 1),
        ...             datetime(2021, 4, 1),
        ...             datetime(2021, 5, 1),
        ...             datetime(2021, 6, 1),
        ...         ],
        ...         "groups": ["A", "B", "A", "B"],
        ...         "values": [0, 1, 2, 3],
        ...     }
        ... ).set_sorted("time")
        >>> df.upsample(
        ...     time_column="time", every="1mo", group_by="groups", maintain_order=True
        ... ).select(pl.all().forward_fill())
        shape: (7, 3)
        ┌─────────────────────┬────────┬────────┐
        │ time                ┆ groups ┆ values │
        │ ---                 ┆ ---    ┆ ---    │
        │ datetime[μs]        ┆ str    ┆ i64    │
        ╞═════════════════════╪════════╪════════╡
        │ 2021-02-01 00:00:00 ┆ A      ┆ 0      │
        │ 2021-03-01 00:00:00 ┆ A      ┆ 0      │
        │ 2021-04-01 00:00:00 ┆ A      ┆ 0      │
        │ 2021-05-01 00:00:00 ┆ A      ┆ 2      │
        │ 2021-04-01 00:00:00 ┆ B      ┆ 1      │
        │ 2021-05-01 00:00:00 ┆ B      ┆ 1      │
        │ 2021-06-01 00:00:00 ┆ B      ┆ 3      │
        └─────────────────────┴────────┴────────┘
        """
        if group_by is None:
            group_by = []
        if isinstance(group_by, str):
            group_by = [group_by]

        every = parse_as_duration_string(every)

        return self._from_pydf(
            self._df.upsample(group_by, time_column, every, maintain_order)
        )
