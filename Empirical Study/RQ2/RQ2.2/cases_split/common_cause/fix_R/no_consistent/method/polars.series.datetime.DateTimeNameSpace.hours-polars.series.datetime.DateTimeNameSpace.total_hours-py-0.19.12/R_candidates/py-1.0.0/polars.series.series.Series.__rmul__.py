    def __rmul__(self, other: Any) -> Series:
        if self.dtype.is_temporal():
            msg = "first cast to integer before multiplying datelike dtypes"
            raise TypeError(msg)
        return self._arithmetic(other, "mul", "mul_<>")
