    def to_pydatetime(self) -> np.ndarray:
        """
        Return the data as an array of :class:`datetime.datetime` objects.

        .. deprecated:: 2.1.0

            The current behavior of dt.to_pydatetime is deprecated.
            In a future version this will return a Series containing python
            datetime objects instead of a ndarray.

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
        # GH#20306
        warnings.warn(
            f"The behavior of {type(self).__name__}.to_pydatetime is deprecated, "
            "in a future version this will return a Series containing python "
            "datetime objects instead of an ndarray. To retain the old behavior, "
            "call `np.array` on the result",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self._get_values().to_pydatetime()
