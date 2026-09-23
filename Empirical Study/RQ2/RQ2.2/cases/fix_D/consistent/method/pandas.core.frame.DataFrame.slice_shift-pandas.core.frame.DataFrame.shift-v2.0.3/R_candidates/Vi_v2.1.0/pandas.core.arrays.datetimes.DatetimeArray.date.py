    @property
    def date(self) -> npt.NDArray[np.object_]:
        """
        Returns numpy array of python :class:`datetime.date` objects.

        Namely, the date part of Timestamps without time and
        timezone information.

        Examples
        --------
        For Series:

        >>> s = pd.Series(["1/1/2020 10:00:00+00:00", "2/1/2020 11:00:00+00:00"])
        >>> s = pd.to_datetime(s)
        >>> s
        0   2020-01-01 10:00:00+00:00
        1   2020-02-01 11:00:00+00:00
        dtype: datetime64[ns, UTC]
        >>> s.dt.date
        0    2020-01-01
        1    2020-02-01
        dtype: object

        For DatetimeIndex:

        >>> idx = pd.DatetimeIndex(["1/1/2020 10:00:00+00:00",
        ...                         "2/1/2020 11:00:00+00:00"])
        >>> idx.date
        array([datetime.date(2020, 1, 1), datetime.date(2020, 2, 1)], dtype=object)
        """
        # If the Timestamps have a timezone that is not UTC,
        # convert them into their i8 representation while
        # keeping their timezone and not using UTC
        timestamps = self._local_timestamps()

        return ints_to_pydatetime(timestamps, box="date", reso=self._creso)
