    def resample(self, rule, how=None, axis=0, fill_method=None, closed=None,
                 label=None, convention='start', kind=None, loffset=None,
                 limit=None, base=0, on=None, level=None):
        """
        Convenience method for frequency conversion and resampling of time
        series.  Object must have a datetime-like index (DatetimeIndex,
        PeriodIndex, or TimedeltaIndex), or pass datetime-like values
        to the on or level keyword.

        Parameters
        ----------
        rule : string
            the offset string or object representing target conversion
        axis : int, optional, default 0
        closed : {'right', 'left'}
            Which side of bin interval is closed
        label : {'right', 'left'}
            Which bin edge label to label bucket with
        convention : {'start', 'end', 's', 'e'}
        loffset : timedelta
            Adjust the resampled time labels
        base : int, default 0
            For frequencies that evenly subdivide 1 day, the "origin" of the
            aggregated intervals. For example, for '5min' frequency, base could
            range from 0 through 4. Defaults to 0
        on : string, optional
            For a DataFrame, column to use instead of index for resampling.
            Column must be datetime-like.

            .. versionadded:: 0.19.0

        level : string or int, optional
            For a MultiIndex, level (name or number) to use for
            resampling.  Level must be datetime-like.

            .. versionadded:: 0.19.0

        Notes
        -----
        To learn more about the offset strings, please see `this link
        <http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases>`__.

        Examples
        --------

        Start by creating a series with 9 one minute timestamps.

        >>> index = pd.date_range('1/1/2000', periods=9, freq='T')
        >>> series = pd.Series(range(9), index=index)
        >>> series
        2000-01-01 00:00:00    0
        2000-01-01 00:01:00    1
        2000-01-01 00:02:00    2
        2000-01-01 00:03:00    3
        2000-01-01 00:04:00    4
        2000-01-01 00:05:00    5
        2000-01-01 00:06:00    6
        2000-01-01 00:07:00    7
        2000-01-01 00:08:00    8
        Freq: T, dtype: int64

        Downsample the series into 3 minute bins and sum the values
        of the timestamps falling into a bin.

        >>> series.resample('3T').sum()
        2000-01-01 00:00:00     3
        2000-01-01 00:03:00    12
        2000-01-01 00:06:00    21
        Freq: 3T, dtype: int64

        Downsample the series into 3 minute bins as above, but label each
        bin using the right edge instead of the left. Please note that the
        value in the bucket used as the label is not included in the bucket,
        which it labels. For example, in the original series the
        bucket ``2000-01-01 00:03:00`` contains the value 3, but the summed
        value in the resampled bucket with the label``2000-01-01 00:03:00``
        does not include 3 (if it did, the summed value would be 6, not 3).
        To include this value close the right side of the bin interval as
        illustrated in the example below this one.

        >>> series.resample('3T', label='right').sum()
        2000-01-01 00:03:00     3
        2000-01-01 00:06:00    12
        2000-01-01 00:09:00    21
        Freq: 3T, dtype: int64

        Downsample the series into 3 minute bins as above, but close the right
        side of the bin interval.

        >>> series.resample('3T', label='right', closed='right').sum()
        2000-01-01 00:00:00     0
        2000-01-01 00:03:00     6
        2000-01-01 00:06:00    15
        2000-01-01 00:09:00    15
        Freq: 3T, dtype: int64

        Upsample the series into 30 second bins.

        >>> series.resample('30S').asfreq()[0:5] #select first 5 rows
        2000-01-01 00:00:00   0.0
        2000-01-01 00:00:30   NaN
        2000-01-01 00:01:00   1.0
        2000-01-01 00:01:30   NaN
        2000-01-01 00:02:00   2.0
        Freq: 30S, dtype: float64

        Upsample the series into 30 second bins and fill the ``NaN``
        values using the ``pad`` method.

        >>> series.resample('30S').pad()[0:5]
        2000-01-01 00:00:00    0
        2000-01-01 00:00:30    0
        2000-01-01 00:01:00    1
        2000-01-01 00:01:30    1
        2000-01-01 00:02:00    2
        Freq: 30S, dtype: int64

        Upsample the series into 30 second bins and fill the
        ``NaN`` values using the ``bfill`` method.

        >>> series.resample('30S').bfill()[0:5]
        2000-01-01 00:00:00    0
        2000-01-01 00:00:30    1
        2000-01-01 00:01:00    1
        2000-01-01 00:01:30    2
        2000-01-01 00:02:00    2
        Freq: 30S, dtype: int64

        Pass a custom function via ``apply``

        >>> def custom_resampler(array_like):
        ...     return np.sum(array_like)+5

        >>> series.resample('3T').apply(custom_resampler)
        2000-01-01 00:00:00     8
        2000-01-01 00:03:00    17
        2000-01-01 00:06:00    26
        Freq: 3T, dtype: int64

        For DataFrame objects, the keyword ``on`` can be used to specify the
        column instead of the index for resampling.

        >>> df = pd.DataFrame(data=9*[range(4)], columns=['a', 'b', 'c', 'd'])
        >>> df['time'] = pd.date_range('1/1/2000', periods=9, freq='T')
        >>> df.resample('3T', on='time').sum()
                             a  b  c  d
        time
        2000-01-01 00:00:00  0  3  6  9
        2000-01-01 00:03:00  0  3  6  9
        2000-01-01 00:06:00  0  3  6  9

        For a DataFrame with MultiIndex, the keyword ``level`` can be used to
        specify on level the resampling needs to take place.

        >>> time = pd.date_range('1/1/2000', periods=5, freq='T')
        >>> df2 = pd.DataFrame(data=10*[range(4)],
                               columns=['a', 'b', 'c', 'd'],
                               index=pd.MultiIndex.from_product([time, [1, 2]])
                               )
        >>> df2.resample('3T', level=0).sum()
                             a  b   c   d
        2000-01-01 00:00:00  0  6  12  18
        2000-01-01 00:03:00  0  4   8  12
        """
        from pandas.core.resample import (resample,
                                          _maybe_process_deprecations)
        axis = self._get_axis_number(axis)
        r = resample(self, freq=rule, label=label, closed=closed,
                     axis=axis, kind=kind, loffset=loffset,
                     convention=convention,
                     base=base, key=on, level=level)
        return _maybe_process_deprecations(r,
                                           how=how,
                                           fill_method=fill_method,
                                           limit=limit)
