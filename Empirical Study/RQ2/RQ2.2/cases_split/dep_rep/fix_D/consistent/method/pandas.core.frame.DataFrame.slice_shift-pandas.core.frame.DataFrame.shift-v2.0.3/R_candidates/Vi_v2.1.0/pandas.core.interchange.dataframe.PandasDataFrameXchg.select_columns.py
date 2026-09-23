    def select_columns(self, indices: Sequence[int]) -> PandasDataFrameXchg:
        if not isinstance(indices, abc.Sequence):
            raise ValueError("`indices` is not a sequence")
        if not isinstance(indices, list):
            indices = list(indices)

        return PandasDataFrameXchg(
            self._df.iloc[:, indices], self._nan_as_null, self._allow_copy
        )
