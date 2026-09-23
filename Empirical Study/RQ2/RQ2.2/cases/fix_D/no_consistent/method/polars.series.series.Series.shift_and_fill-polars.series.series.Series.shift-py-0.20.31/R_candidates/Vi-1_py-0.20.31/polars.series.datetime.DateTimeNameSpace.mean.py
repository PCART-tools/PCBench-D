    def mean(self) -> TemporalLiteral | float | None:
        """
        Return mean as python DateTime.

        Examples
        --------
        >>> from datetime import datetime
        >>> s = pl.Series(
        ...     [datetime(2001, 1, 1), datetime(2001, 1, 2), datetime(2001, 1, 3)]
        ... )
        >>> s.dt.mean()
        datetime.datetime(2001, 1, 2, 0, 0)
        """
        s = wrap_s(self._s)
        out = s.mean()
        if out is not None:
            if s.dtype == Date:
                return to_py_date(int(out))  # type: ignore[arg-type]
            elif s.dtype in (Datetime, Duration, Time):
                return out  # type: ignore[return-value]
            else:
                return to_py_datetime(int(out), s.dtype.time_unit)  # type: ignore[arg-type, attr-defined]
        return None
