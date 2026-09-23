    def get_ftype_counts(self):
        """Return the counts of ftypes in this object."""
        from pandas import Series
        return Series(self._data.get_ftype_counts())
