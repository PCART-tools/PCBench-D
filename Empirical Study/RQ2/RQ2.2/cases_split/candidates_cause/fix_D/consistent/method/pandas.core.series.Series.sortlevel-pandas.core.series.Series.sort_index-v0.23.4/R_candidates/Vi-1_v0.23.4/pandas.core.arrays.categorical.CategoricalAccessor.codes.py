    @property
    def codes(self):
        from pandas import Series
        return Series(self.categorical.codes, index=self.index)
