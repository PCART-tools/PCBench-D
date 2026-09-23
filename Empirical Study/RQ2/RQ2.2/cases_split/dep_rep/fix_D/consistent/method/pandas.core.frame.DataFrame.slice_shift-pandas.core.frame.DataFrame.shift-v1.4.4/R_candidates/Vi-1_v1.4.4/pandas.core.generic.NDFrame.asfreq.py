    @doc(**_shared_doc_kwargs)
    def asfreq(
        self: NDFrameT,
        freq,
        method=None,
        how: str | None = None,
        normalize: bool_t = False,
        fill_value=None,
    ) -> NDFrameT:
        """
        Convert time series to specified frequency.

        Returns the original data conformed to a new index with the specified
        frequency.

        If the index of this {klass} is a :class:`~pandas.PeriodIndex`, the new index
        is the result of transforming the original index with
        :meth:`PeriodIndex.asfreq <pandas.PeriodIndex.asfreq>` (so the original index
        will map one-to-one to the new index).

        Otherwise, the new index will be equivalent to ``pd.date_range(start, end,
        freq=freq)`` where ``start`` and ``end`` are, respectively, the first and
        last entries in the original index (see :func:`pandas.date_range`). The
        values corresponding to any timesteps in the new index which were not present
        in the original index will be null (``NaN``), unless a method for filling
        such unknowns is provided (see the ``method`` parameter below).

        The :meth:`resample` method is more appropriate if an operation on each group of
        timesteps (such as an aggregate) is necessary to represent the data at the new
        frequency.

        Parameters
        ----------
        freq : DateOffset or str
            Frequency DateOffset or string.
        method : {{'backfill'/'bfill', 'pad'/'ffill'}}, default None
            Method to use for filling holes in reindexed Series (note this
            does not fill NaNs that already were present):

            * 'pad' / 'ffill': propagate last valid observation forward to next
              valid
            * 'backfill' / 'bfill': use NEXT valid observation to fill.
        how : {{'start', 'end'}}, default end
            For PeriodIndex only (see PeriodIndex.asfreq).
        normalize : bool, default False
            Whether to reset output index to midnight.
        fill_value : scalar, optional
            Value to use for missing values, applied during upsampling (note
            this does not fill NaNs that already were present).

        Returns
        -------
        {klass}
            {klass} object reindexed to the specified frequency.

        See Also
        --------
        reindex : Conform DataFrame to new index with optional filling logic.

        Notes
        -----
        To learn more about the frequency strings, please see `this link
        <https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases>`__.

        Examples
        --------
        Start by creating a series with 4 one minute timestamps.

        >>> index = pd.date_range('1/1/2000', periods=4, freq='T')
        >>> series = pd.Series([0.0, None, 2.0, 3.0], index=index)
        >>> df = pd.DataFrame({{'s': series}})
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

        return asfreq(
            self,
            freq,
            method=method,
            how=how,
            normalize=normalize,
            fill_value=fill_value,
        )
