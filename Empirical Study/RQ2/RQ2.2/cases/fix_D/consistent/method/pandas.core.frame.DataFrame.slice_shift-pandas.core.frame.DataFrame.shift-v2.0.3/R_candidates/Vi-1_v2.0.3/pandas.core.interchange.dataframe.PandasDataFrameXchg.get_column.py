    def get_column(self, i: int) -> PandasColumn:
        return PandasColumn(self._df.iloc[:, i], allow_copy=self._allow_copy)
