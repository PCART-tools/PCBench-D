    def cast_time_unit(self, time_unit: TimeUnit) -> Series:
        """
        Cast the underlying data to another time unit. This may lose precision.

        Parameters
        ----------
        time_unit : {'ns', 'us', 'ms'}
            Unit of time for the `Datetime` Series.

        Examples
        --------
        >>> from datetime import datetime
        >>> start = datetime(2001, 1, 1)
        >>> stop = datetime(2001, 1, 3)
        >>> date = pl.datetime_range(start, stop, "1d", eager=True).alias("datetime")
        >>> date
        shape: (3,)
        Series: 'datetime' [datetime[μs]]
        [
                2001-01-01 00:00:00
                2001-01-02 00:00:00
                2001-01-03 00:00:00
        ]
        >>> date.dt.cast_time_unit("ms").alias("time_unit_ms")
        shape: (3,)
        Series: 'time_unit_ms' [datetime[ms]]
        [
                2001-01-01 00:00:00
                2001-01-02 00:00:00
                2001-01-03 00:00:00
        ]
        >>> date.dt.cast_time_unit("ns").alias("time_unit_ns")
        shape: (3,)
        Series: 'time_unit_ns' [datetime[ns]]
        [
                2001-01-01 00:00:00
                2001-01-02 00:00:00
                2001-01-03 00:00:00
        ]

        """
