    def epoch(self, time_unit: EpochTimeUnit = "us") -> Series:
        """
        Get the time passed since the Unix EPOCH in the give time unit.

        Parameters
        ----------
        time_unit : {'us', 'ns', 'ms', 's', 'd'}
            Unit of time.

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
        >>> date.dt.epoch().alias("epoch_ns")
        shape: (3,)
        Series: 'epoch_ns' [i64]
        [
                978307200000000
                978393600000000
                978480000000000
        ]
        >>> date.dt.epoch(time_unit="s").alias("epoch_s")
        shape: (3,)
        Series: 'epoch_s' [i64]
        [
                978307200
                978393600
                978480000
        ]
        """
