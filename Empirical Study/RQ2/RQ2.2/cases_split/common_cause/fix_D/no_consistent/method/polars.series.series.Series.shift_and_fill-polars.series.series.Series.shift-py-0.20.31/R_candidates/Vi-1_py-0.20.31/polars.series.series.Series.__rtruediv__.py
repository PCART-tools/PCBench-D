    def __rtruediv__(self, other: Any) -> Series:
        if self.dtype.is_temporal():
            msg = "first cast to integer before dividing datelike dtypes"
            raise TypeError(msg)
        if self.dtype.is_float():
            self.__rfloordiv__(other)

        if isinstance(other, int):
            other = float(other)
        return self.cast(Float64).__rfloordiv__(other)
