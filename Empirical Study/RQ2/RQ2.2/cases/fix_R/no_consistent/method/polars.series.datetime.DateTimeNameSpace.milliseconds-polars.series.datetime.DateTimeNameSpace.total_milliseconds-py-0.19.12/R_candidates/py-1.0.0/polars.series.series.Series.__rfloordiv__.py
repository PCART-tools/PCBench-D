    def __rfloordiv__(self, other: Any) -> Series:
        if self.dtype.is_temporal():
            msg = "first cast to integer before dividing datelike dtypes"
            raise TypeError(msg)
        return self._arithmetic(other, "div", "div_<>_rhs")
