    def __eq__(self, other: Any) -> DataFrame:  # type: ignore[override]
        return self._comp(other, "eq")
