    def __ne__(self, other: Any) -> DataFrame:  # type: ignore[override]
        return self._comp(other, "neq")
