    def __gt__(self, other: Any) -> DataFrame:
        return self._comp(other, "gt")
