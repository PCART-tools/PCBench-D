    def get_dtype_counts(self):
        """ return the counts of dtypes in this frame """
        from pandas import Series
        return Series(self._data.get_dtype_counts())
