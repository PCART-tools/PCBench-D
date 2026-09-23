    def value_counts(self, dropna: bool = True) -> Series:
        from pandas.core.algorithms import value_counts_internal as value_counts

        result = value_counts(self._ndarray, dropna=dropna).astype("Int64")
        result.index = result.index.astype(self.dtype)
        return result
