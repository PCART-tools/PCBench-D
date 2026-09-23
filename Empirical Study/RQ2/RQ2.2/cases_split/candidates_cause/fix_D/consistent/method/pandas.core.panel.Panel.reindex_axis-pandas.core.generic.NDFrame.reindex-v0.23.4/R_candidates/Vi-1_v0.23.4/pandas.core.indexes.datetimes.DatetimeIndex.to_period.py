    def to_period(self, freq=None):
        """
        Cast to PeriodIndex at a particular frequency.

        Converts DatetimeIndex to PeriodIndex.

        Parameters
        ----------
        freq : string or Offset, optional
            One of pandas' :ref:`offset strings <timeseries.offset_aliases>`
            or an Offset object. Will be inferred by default.

        Returns
        -------
        PeriodIndex

        Raises
        ------
        ValueError
            When converting a DatetimeIndex with non-regular values, so that a
            frequency cannot be inferred.

        Examples
        --------
        >>> df = pd.DataFrame({"y": [1,2,3]},
        ...                   index=pd.to_datetime(["2000-03-31 00:00:00",
        ...                                         "2000-05-31 00:00:00",
        ...                                         "2000-08-31 00:00:00"]))
        >>> df.index.to_period("M")
        PeriodIndex(['2000-03', '2000-05', '2000-08'],
                    dtype='period[M]', freq='M')

        Infer the daily frequency

        >>> idx = pd.date_range("2017-01-01", periods=2)
        >>> idx.to_period()
        PeriodIndex(['2017-01-01', '2017-01-02'],
                    dtype='period[D]', freq='D')

        See also
        --------
        pandas.PeriodIndex: Immutable ndarray holding ordinal values
        pandas.DatetimeIndex.to_pydatetime: Return DatetimeIndex as object
        """
        from pandas.core.indexes.period import PeriodIndex

        if freq is None:
            freq = self.freqstr or self.inferred_freq

            if freq is None:
                msg = ("You must pass a freq argument as "
                       "current index has none.")
                raise ValueError(msg)

            freq = get_period_alias(freq)

        return PeriodIndex(self.values, name=self.name, freq=freq, tz=self.tz)
