    def timestamp(self, time_unit: TimeUnit = "us") -> Series:
        """
        Return a timestamp in the given time unit.

        Parameters
        ----------
        time_unit : {'us', 'ns', 'ms'}
            Time unit.

        Examples
        --------
        >>> from datetime import datetime
        >>> start = datetime(2001, 1, 1)
        >>> stop = datetime(2001, 1, 3)
        >>> date = pl.datetime_range(start, stop, interval="1d", eager=True).alias(
        ...     "datetime"
        ... )
        >>> date
        shape: (3,)
        Series: 'datetime' [datetime[μs]]
        [
                2001-01-01 00:00:00
                2001-01-02 00:00:00
                2001-01-03 00:00:00
        ]
        >>> date.dt.timestamp().alias("timestamp_us")
        shape: (3,)
        Series: 'timestamp_us' [i64]
        [
                978307200000000
                978393600000000
                978480000000000
        ]
        >>> date.dt.timestamp("ns").alias("timestamp_ns")
        shape: (3,)
        Series: 'timestamp_ns' [i64]
        [
                978307200000000000
                978393600000000000
                978480000000000000
        ]

        """
