    def __floordiv__(self, other: Any) -> Series | Expr:
        if isinstance(other, pl.Expr):
            return F.lit(self) // other
        if self.dtype.is_temporal():
            raise TypeError("first cast to integer before dividing datelike dtypes")

        if not isinstance(other, pl.Expr):
            other = F.lit(other)
        return self.to_frame().select_seq(F.col(self.name) // other).to_series()
