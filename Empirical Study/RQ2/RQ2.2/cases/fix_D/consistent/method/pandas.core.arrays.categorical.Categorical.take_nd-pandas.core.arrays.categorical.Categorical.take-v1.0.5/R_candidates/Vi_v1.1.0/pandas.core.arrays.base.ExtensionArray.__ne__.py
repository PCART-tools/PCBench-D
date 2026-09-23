    def __ne__(self, other: Any) -> ArrayLike:
        """
        Return for `self != other` (element-wise in-equality).
        """
        return ~(self == other)
