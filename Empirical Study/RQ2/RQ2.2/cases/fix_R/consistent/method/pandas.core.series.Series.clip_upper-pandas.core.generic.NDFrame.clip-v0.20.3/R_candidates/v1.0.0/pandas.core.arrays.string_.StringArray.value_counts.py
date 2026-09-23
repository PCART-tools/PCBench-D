    def value_counts(self, dropna=False):
        from pandas import value_counts

        return value_counts(self._ndarray, dropna=dropna).astype("Int64")
