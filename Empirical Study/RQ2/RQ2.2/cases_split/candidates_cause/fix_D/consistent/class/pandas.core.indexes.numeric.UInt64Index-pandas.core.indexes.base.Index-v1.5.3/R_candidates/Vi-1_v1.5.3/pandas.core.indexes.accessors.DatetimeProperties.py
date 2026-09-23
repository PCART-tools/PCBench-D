@delegate_names(
    delegate=DatetimeArray, accessors=DatetimeArray._datetimelike_ops, typ="property"
)
@delegate_names(
    delegate=DatetimeArray, accessors=DatetimeArray._datetimelike_methods, typ="method"
)
class DatetimeProperties(Properties):
    """
    Accessor object for datetimelike properties of the Series values.

    Examples
    --------
    >>> seconds_series = pd.Series(pd.date_range("2000-01-01", periods=3, freq="s"))
    >>> seconds_series
    0   2000-01-01 00:00:00
    1   2000-01-01 00:00:01
    2   2000-01-01 00:00:02
    dtype: datetime64[ns]
    >>> seconds_series.dt.second
    0    0
    1    1
    2    2
    dtype: int64

    >>> hours_series = pd.Series(pd.date_range("2000-01-01", periods=3, freq="h"))
    >>> hours_series
    0   2000-01-01 00:00:00
    1   2000-01-01 01:00:00
    2   2000-01-01 02:00:00
    dtype: datetime64[ns]
    >>> hours_series.dt.hour
    0    0
    1    1
    2    2
    dtype: int64

    >>> quarters_series = pd.Series(pd.date_range("2000-01-01", periods=3, freq="q"))
    >>> quarters_series
    0   2000-03-31
    1   2000-06-30
    2   2000-09-30
    dtype: datetime64[ns]
    >>> quarters_series.dt.quarter
    0    1
    1    2
    2    3
    dtype: int64

    Returns a Series indexed like the original Series.
    Raises TypeError if the Series does not contain datetimelike values.
    """

    def to_pydatetime(self) -> np.ndarray:
        """
        Return the data as an array of :class:`datetime.datetime` objects.

        Timezone information is retained if present.

        .. warning::

           Python's datetime uses microsecond resolution, which is lower than
           pandas (nanosecond). The values are truncated.

        Returns
        -------
        numpy.ndarray
            Object dtype array containing native Python datetime objects.

        See Also
        --------
        datetime.datetime : Standard library value for a datetime.

        Examples
        --------
        >>> s = pd.Series(pd.date_range('20180310', periods=2))
        >>> s
        0   2018-03-10
        1   2018-03-11
        dtype: datetime64[ns]

        >>> s.dt.to_pydatetime()
        array([datetime.datetime(2018, 3, 10, 0, 0),
               datetime.datetime(2018, 3, 11, 0, 0)], dtype=object)

        pandas' nanosecond precision is truncated to microseconds.

        >>> s = pd.Series(pd.date_range('20180310', periods=2, freq='ns'))
        >>> s
        0   2018-03-10 00:00:00.000000000
        1   2018-03-10 00:00:00.000000001
        dtype: datetime64[ns]

        >>> s.dt.to_pydatetime()
        array([datetime.datetime(2018, 3, 10, 0, 0),
               datetime.datetime(2018, 3, 10, 0, 0)], dtype=object)
        """
        return self._get_values().to_pydatetime()

    @property
    def freq(self):
        return self._get_values().inferred_freq

    def isocalendar(self) -> DataFrame:
        """
        Calculate year, week, and day according to the ISO 8601 standard.

        .. versionadded:: 1.1.0

        Returns
        -------
        DataFrame
            With columns year, week and day.

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

    @property
    def weekofyear(self):
        """
        The week ordinal of the year according to the ISO 8601 standard.

        .. deprecated:: 1.1.0

        Series.dt.weekofyear and Series.dt.week have been deprecated.  Please
        call :func:`Series.dt.isocalendar` and access the ``week`` column
        instead.
        """
        warnings.warn(
            "Series.dt.weekofyear and Series.dt.week have been deprecated. "
            "Please use Series.dt.isocalendar().week instead.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        week_series = self.isocalendar().week
        week_series.name = self.name
        if week_series.hasnans:
            return week_series.astype("float64")
        return week_series.astype("int64")

    week = weekofyear
