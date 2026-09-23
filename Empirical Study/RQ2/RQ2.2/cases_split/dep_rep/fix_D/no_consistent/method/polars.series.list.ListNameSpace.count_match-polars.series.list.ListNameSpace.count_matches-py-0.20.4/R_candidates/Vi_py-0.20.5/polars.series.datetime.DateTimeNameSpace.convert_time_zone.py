    def convert_time_zone(self, time_zone: str) -> Series:
        """
        Convert to given time zone for a Series of type Datetime.

        Parameters
        ----------
        time_zone
            Time zone for the `Datetime` Series.

        Examples
        --------
        >>> from datetime import datetime
        >>> start = datetime(2020, 3, 1)
        >>> stop = datetime(2020, 5, 1)
        >>> date = pl.datetime_range(
        ...     start, stop, "1mo", time_zone="UTC", eager=True
        ... ).alias("datetime")
        >>> date
        shape: (3,)
        Series: 'datetime' [datetime[μs, UTC]]
        [
                2020-03-01 00:00:00 UTC
                2020-04-01 00:00:00 UTC
                2020-05-01 00:00:00 UTC
        ]
        >>> date = date.dt.convert_time_zone("Europe/London").alias("London")
        >>> date
        shape: (3,)
        Series: 'London' [datetime[μs, Europe/London]]
        [
            2020-03-01 00:00:00 GMT
            2020-04-01 01:00:00 BST
            2020-05-01 01:00:00 BST
        ]
        """
