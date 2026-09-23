    def mean(self) -> dt.date | dt.datetime | None:
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
                return _to_python_date(int(out))
            else:
                return _to_python_datetime(int(out), s.dtype.time_unit)  # type: ignore[attr-defined]
        return None
