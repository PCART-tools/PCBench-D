    @property
    def codes(self):
        """
        Return Series of codes as well as the index.
        """
        from pandas import Series

        return Series(self._parent.codes, index=self._index)
