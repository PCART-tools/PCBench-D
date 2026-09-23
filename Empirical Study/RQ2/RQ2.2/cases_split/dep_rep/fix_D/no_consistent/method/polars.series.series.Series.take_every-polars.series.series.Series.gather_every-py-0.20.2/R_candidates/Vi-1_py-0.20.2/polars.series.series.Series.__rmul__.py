    def __rmul__(self, other: Any) -> Series:
        if self.dtype.is_temporal():
            raise TypeError("first cast to integer before multiplying datelike dtypes")
        return self._arithmetic(other, "mul", "mul_<>")
