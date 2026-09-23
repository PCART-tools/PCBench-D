    def value_counts(self, dropna: bool = True) -> Series:
        from pandas import value_counts

        result = value_counts(self._ndarray, dropna=dropna).astype("Int64")
        result.index = result.index.astype(self.dtype)
        return result
