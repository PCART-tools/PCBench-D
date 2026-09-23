    def get_column_by_name(self, name: str) -> PandasColumn:
        return PandasColumn(self._df[name], allow_copy=self._allow_copy)
