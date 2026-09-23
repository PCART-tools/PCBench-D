    def __or__(self, other: Series) -> Self:
        if not isinstance(other, Series):
            other = Series([other])
        return self._from_pyseries(self._s.bitor(other._s))
