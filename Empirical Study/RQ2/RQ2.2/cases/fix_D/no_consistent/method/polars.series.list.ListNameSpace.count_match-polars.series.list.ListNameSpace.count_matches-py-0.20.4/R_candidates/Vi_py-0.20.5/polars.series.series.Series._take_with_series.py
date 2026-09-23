    def _take_with_series(self, s: Series) -> Series:
        return self._from_pyseries(self._s.take_with_series(s._s))
