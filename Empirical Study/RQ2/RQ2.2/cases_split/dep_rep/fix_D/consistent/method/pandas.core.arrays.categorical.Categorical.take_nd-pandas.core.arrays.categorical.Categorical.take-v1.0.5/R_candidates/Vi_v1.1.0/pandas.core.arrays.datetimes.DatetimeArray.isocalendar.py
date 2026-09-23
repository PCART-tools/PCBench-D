    def isocalendar(self):
        """
        Returns a DataFrame with the year, week, and day calculated according to
        the ISO 8601 standard.

        .. versionadded:: 1.1.0

        Returns
        -------
        DataFrame
            with columns year, week and day

        See Also
        --------
        Timestamp.isocalendar
        datetime.date.isocalendar

        Examples
        --------
        >>> idx = pd.date_range(start='2019-12-29', freq='D', periods=4)
        >>> idx.isocalendar()
                    year  week  day
        2019-12-29  2019    52    7
        2019-12-30  2020     1    1
        2019-12-31  2020     1    2
        2020-01-01  2020     1    3
        >>> idx.isocalendar().week
        2019-12-29    52
        2019-12-30     1
        2019-12-31     1
        2020-01-01     1
        Freq: D, Name: week, dtype: UInt32
        """
        from pandas import DataFrame

        if self.tz is not None and not timezones.is_utc(self.tz):
            values = self._local_timestamps()
        else:
            values = self.asi8
        sarray = fields.build_isocalendar_sarray(values)
        iso_calendar_df = DataFrame(
            sarray, columns=["year", "week", "day"], dtype="UInt32"
        )
        if self._hasnans:
            iso_calendar_df.iloc[self._isnan] = None
        return iso_calendar_df
