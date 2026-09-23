    def with_time_unit(self, time_unit: TimeUnit) -> Series:
        """
        Set time unit a Series of dtype Datetime or Duration.

        This does not modify underlying data, and should be used to fix an incorrect
        time unit.

        Parameters
        ----------
        time_unit : {'ns', 'us', 'ms'}
            Unit of time for the `Datetime` Series.

        Examples
        --------
        >>> from datetime import datetime
        >>> s = pl.Series(
        ...     "datetime",
        ...     [datetime(2001, 1, 1), datetime(2001, 1, 2), datetime(2001, 1, 3)],
        ...     dtype=pl.Datetime(time_unit="ns"),
        ... )
        >>> s.dt.with_time_unit("us")
        shape: (3,)
        Series: 'datetime' [datetime[μs]]
        [
                +32971-04-28 00:00:00
                +32974-01-22 00:00:00
                +32976-10-18 00:00:00
        ]
        """
