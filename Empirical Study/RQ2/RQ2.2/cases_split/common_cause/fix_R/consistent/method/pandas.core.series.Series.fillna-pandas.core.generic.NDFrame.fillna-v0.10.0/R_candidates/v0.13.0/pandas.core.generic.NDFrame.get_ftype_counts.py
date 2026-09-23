    def get_ftype_counts(self):
        """ return the counts of ftypes in this frame """
        from pandas import Series
        return Series(self._data.get_ftype_counts())
