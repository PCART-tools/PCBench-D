    def __mul__(self, other: Any) -> Series | DataFrame | Expr:
        if isinstance(other, pl.Expr):
            return F.lit(self) * other
        if self.dtype.is_temporal():
            msg = "first cast to integer before multiplying datelike dtypes"
            raise TypeError(msg)
        elif isinstance(other, pl.DataFrame):
            return other * self
        else:
            return self._arithmetic(other, "mul", "mul_<>")
