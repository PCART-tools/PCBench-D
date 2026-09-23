    def __le__(self, other: Any) -> DataFrame:
        return self._comp(other, "lt_eq")
