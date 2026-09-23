    def median(self) -> TemporalLiteral | float | None:
        """
        Return median as python DateTime.

        Examples
        --------
        >>> from datetime import datetime
        >>> date = pl.datetime_range(
        ...     datetime(2001, 1, 1), datetime(2001, 1, 3), "1d", eager=True
        ... ).alias("datetime")
        >>> date
        shape: (3,)
        Series: 'datetime' [datetime[μs]]
        [
                2001-01-01 00:00:00
                2001-01-02 00:00:00
                2001-01-03 00:00:00
        ]
        >>> date.dt.median()
        datetime.datetime(2001, 1, 2, 0, 0)
        """
        s = wrap_s(self._s)
        out = s.median()
        if out is not None:
            if s.dtype == Date:
                return _to_python_date(int(out))  # type: ignore[arg-type]
            elif s.dtype == Datetime:
                return out  # type: ignore[return-value]
            else:
                return _to_python_datetime(int(out), s.dtype.time_unit)  # type: ignore[arg-type, attr-defined]
        return None
