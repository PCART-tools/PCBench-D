    def get_dtype_counts(self):
        """ Return the counts of dtypes in this object """
        from pandas import Series
        return Series(self._data.get_dtype_counts())
