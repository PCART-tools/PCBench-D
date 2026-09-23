    def __xor__(self, other: Any) -> Self:
        if not isinstance(other, Series):
            other = Series([other])
        return self._from_pyseries(self._s.bitxor(other._s))
