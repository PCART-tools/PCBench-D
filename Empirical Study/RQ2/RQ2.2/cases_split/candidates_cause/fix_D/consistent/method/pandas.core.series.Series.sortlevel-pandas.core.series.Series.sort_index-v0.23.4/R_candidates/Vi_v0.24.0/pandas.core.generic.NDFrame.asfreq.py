    def asfreq(self, freq, method=None, how=None, normalize=False,
               fill_value=None):
        """
        Convert TimeSeries to specified frequency.

        Optionally provide filling method to pad/backfill missing values.

        Returns the original data conformed to a new index with the specified
        frequency. ``resample`` is more appropriate if an operation, such as
        summarization, is necessary to represent the data at the new frequency.

        Parameters
        ----------
        freq : DateOffset object, or string
        method : {'backfill'/'bfill', 'pad'/'ffill'}, default None
            Method to use for filling holes in reindexed Series (note this
            does not fill NaNs that already were present):

            * 'pad' / 'ffill': propagate last valid observation forward to next
              valid
            * 'backfill' / 'bfill': use NEXT valid observation to fill
        how : {'start', 'end'}, default end
            For PeriodIndex only, see PeriodIndex.asfreq
        normalize : bool, default False
            Whether to reset output index to midnight
        fill_value : scalar, optional
            Value to use for missing values, applied during upsampling (note
            this does not fill NaNs that already were present).

            .. versionadded:: 0.20.0

        Returns
        -------
        converted : same type as caller

        See Also
        --------
        reindex

        Notes
        -----
        To learn more about the frequency strings, please see `this link
        <http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases>`__.

        Examples
        --------

        Start by creating a series with 4 one minute timestamps.

        >>> index = pd.date_range('1/1/2000', periods=4, freq='T')
        >>> series = pd.Series([0.0, None, 2.0, 3.0], index=index)
        >>> df = pd.DataFrame({'s':series})
        >>> df
                               s
        2000-01-01 00:00:00    0.0
        2000-01-01 00:01:00    NaN
        2000-01-01 00:02:00    2.0
        2000-01-01 00:03:00    3.0

        Upsample the series into 30 second bins.

        >>> df.asfreq(freq='30S')
                               s
        2000-01-01 00:00:00    0.0
        2000-01-01 00:00:30    NaN
        2000-01-01 00:01:00    NaN
        2000-01-01 00:01:30    NaN
        2000-01-01 00:02:00    2.0
        2000-01-01 00:02:30    NaN
        2000-01-01 00:03:00    3.0

        Upsample again, providing a ``fill value``.

        >>> df.asfreq(freq='30S', fill_value=9.0)
                               s
        2000-01-01 00:00:00    0.0
        2000-01-01 00:00:30    9.0
        2000-01-01 00:01:00    NaN
        2000-01-01 00:01:30    9.0
        2000-01-01 00:02:00    2.0
        2000-01-01 00:02:30    9.0
        2000-01-01 00:03:00    3.0

        Upsample again, providing a ``method``.

        >>> df.asfreq(freq='30S', method='bfill')
                               s
        2000-01-01 00:00:00    0.0
        2000-01-01 00:00:30    NaN
        2000-01-01 00:01:00    NaN
        2000-01-01 00:01:30    2.0
        2000-01-01 00:02:00    2.0
        2000-01-01 00:02:30    3.0
        2000-01-01 00:03:00    3.0
        """
        from pandas.core.resample import asfreq
        return asfreq(self, freq, method=method, how=how, normalize=normalize,
                      fill_value=fill_value)
