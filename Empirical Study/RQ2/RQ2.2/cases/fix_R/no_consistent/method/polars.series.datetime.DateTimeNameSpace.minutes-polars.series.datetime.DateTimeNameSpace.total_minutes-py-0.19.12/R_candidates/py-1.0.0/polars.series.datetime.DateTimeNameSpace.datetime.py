    @deprecate_function("Use `dt.replace_time_zone(None)` instead.", version="0.20.4")
    def datetime(self) -> Series:
        """
        Extract (local) datetime.

        .. deprecated:: 0.20.4
            Use `dt.replace_time_zone(None)` instead.

        Applies to Datetime columns.

        Returns
        -------
        Series
            Series of data type :class:`Datetime`.

        Examples
        --------
        >>> from datetime import datetime
        >>> ser = pl.Series([datetime(2021, 1, 2, 5)]).dt.replace_time_zone(
        ...     "Asia/Kathmandu"
        ... )
        >>> ser
        shape: (1,)
        Series: '' [datetime[μs, Asia/Kathmandu]]
        [
                2021-01-02 05:00:00 +0545
        ]
        >>> ser.dt.datetime()  # doctest: +SKIP
        shape: (1,)
        Series: '' [datetime[μs]]
        [
                2021-01-02 05:00:00
        ]
        """
