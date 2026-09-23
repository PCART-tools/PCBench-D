    def _take_with_series(self, s: Series) -> DataFrame:
        return self._from_pydf(self._df.take_with_series(s._s))
