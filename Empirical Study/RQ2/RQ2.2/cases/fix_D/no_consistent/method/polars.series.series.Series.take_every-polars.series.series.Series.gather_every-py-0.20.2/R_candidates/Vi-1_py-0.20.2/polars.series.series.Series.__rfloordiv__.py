    def __rfloordiv__(self, other: Any) -> Series:
        if self.dtype.is_temporal():
            raise TypeError("first cast to integer before dividing datelike dtypes")
        return self._arithmetic(other, "div", "div_<>_rhs")
