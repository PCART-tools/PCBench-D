    def asfreq(self, freq, method=None, how=None, normalize=False):
        """
        Convert TimeSeries to specified frequency.

        Optionally provide filling method to pad/backfill missing values.

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

        Returns
        -------
        converted : type of caller

        Notes
        -----
        To learn more about the frequency strings, please see `this link
        <http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases>`__.
        """
        from pandas.tseries.resample import asfreq
        return asfreq(self, freq, method=method, how=how, normalize=normalize)
