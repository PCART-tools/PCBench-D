    def quantile(self, q=0.5):
        """
        Return value at the given quantile, a la scoreatpercentile in
        scipy.stats

        Parameters
        ----------
        q : quantile
            0 <= q <= 1

        Returns
        -------
        quantile : float
        """
        valid_values = self.dropna().values
        if len(valid_values) == 0:
            return pa.NA
        result = _quantile(valid_values, q * 100)
        if result.dtype == _TD_DTYPE:
            from pandas.tseries.timedeltas import to_timedelta
            return to_timedelta(result)

        return result
