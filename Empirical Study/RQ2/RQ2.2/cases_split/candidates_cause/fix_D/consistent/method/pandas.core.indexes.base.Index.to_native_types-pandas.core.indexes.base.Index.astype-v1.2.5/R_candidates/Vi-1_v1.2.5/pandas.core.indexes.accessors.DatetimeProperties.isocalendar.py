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
        Timestamp.isocalendar : Function return a 3-tuple containing ISO year,
            week number, and weekday for the given Timestamp object.
        datetime.date.isocalendar : Return a named tuple object with
            three components: year, week and weekday.

        Examples
        --------
        >>> ser = pd.to_datetime(pd.Series(["2010-01-01", pd.NaT]))
        >>> ser.dt.isocalendar()
           year  week  day
        0  2009    53     5
        1  <NA>  <NA>  <NA>
        >>> ser.dt.isocalendar().week
        0      53
        1    <NA>
        Name: week, dtype: UInt32
        """
        return self._get_values().isocalendar().set_index(self._parent.index)
