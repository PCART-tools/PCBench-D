    def __ne__(self, other: Any) -> ArrayLike:  # type: ignore[override]
        """
        Return for `self != other` (element-wise in-equality).
        """
        return ~(self == other)
