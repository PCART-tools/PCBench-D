    def max(self) -> dt.date | dt.datetime | dt.timedelta | None:
        """
        Return maximum as Python datetime.

        Examples
        --------
        >>> from datetime import date
        >>> s = pl.Series([date(2001, 1, 1), date(2001, 1, 2), date(2001, 1, 3)])
        >>> s.dt.max()
        datetime.date(2001, 1, 3)
        """
        return wrap_s(self._s).max()  # type: ignore[return-value]
