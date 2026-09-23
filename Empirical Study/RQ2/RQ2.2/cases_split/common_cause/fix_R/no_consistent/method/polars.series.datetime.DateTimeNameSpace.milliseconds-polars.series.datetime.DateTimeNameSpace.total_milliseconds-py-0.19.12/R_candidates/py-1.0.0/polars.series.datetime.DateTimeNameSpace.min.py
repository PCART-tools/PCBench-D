    def min(self) -> dt.date | dt.datetime | dt.timedelta | None:
        """
        Return minimum as Python datetime.

        Examples
        --------
        >>> from datetime import date
        >>> s = pl.Series([date(2001, 1, 1), date(2001, 1, 2), date(2001, 1, 3)])
        >>> s.dt.min()
        datetime.date(2001, 1, 1)
        """
        return wrap_s(self._s).min()  # type: ignore[return-value]
