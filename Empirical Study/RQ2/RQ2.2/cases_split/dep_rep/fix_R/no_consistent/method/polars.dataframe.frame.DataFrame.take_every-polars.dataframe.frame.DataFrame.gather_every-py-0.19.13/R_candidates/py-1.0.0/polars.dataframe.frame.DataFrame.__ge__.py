    def __ge__(self, other: Any) -> DataFrame:
        return self._comp(other, "gt_eq")
