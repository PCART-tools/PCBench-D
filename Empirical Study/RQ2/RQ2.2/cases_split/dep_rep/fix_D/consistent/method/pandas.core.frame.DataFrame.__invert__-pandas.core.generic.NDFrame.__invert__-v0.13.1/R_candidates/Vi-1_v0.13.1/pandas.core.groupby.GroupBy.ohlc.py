    def ohlc(self):
        """
        Compute sum of values, excluding missing values

        For multiple groupings, the result index will be a MultiIndex

        """
        return self._cython_agg_general('ohlc')
