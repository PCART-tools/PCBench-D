    def ohlc(self):
        """
        Compute sum of values, excluding missing values

        For multiple groupings, the result index will be a MultiIndex
        """
        return self._apply_to_column_groupbys(
            lambda x: x._cython_agg_general('ohlc'))
