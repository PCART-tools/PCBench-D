    def _replace(self, column: str, new_column: Series) -> Self:
        """Replace a column by a new Series (in place)."""
        self._df.replace(column, new_column._s)
        return self
