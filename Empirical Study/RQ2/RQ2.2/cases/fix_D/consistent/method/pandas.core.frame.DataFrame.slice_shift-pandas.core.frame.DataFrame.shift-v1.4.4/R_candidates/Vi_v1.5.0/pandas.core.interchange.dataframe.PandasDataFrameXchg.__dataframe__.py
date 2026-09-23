    def __dataframe__(
        self, nan_as_null: bool = False, allow_copy: bool = True
    ) -> PandasDataFrameXchg:
        return PandasDataFrameXchg(self._df, nan_as_null, allow_copy)
