    def __truediv__(self, other: Any) -> Series | Expr:
        if isinstance(other, pl.Expr):
            return F.lit(self) / other
        if self.dtype.is_temporal():
            raise TypeError("first cast to integer before dividing datelike dtypes")

        # this branch is exactly the floordiv function without rounding the floats
        if self.dtype.is_float() or self.dtype == Decimal:
            return self._arithmetic(other, "div", "div_<>")

        return self.cast(Float64) / other
