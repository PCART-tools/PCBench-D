    def __mod__(self, other: Any) -> Series | Expr:
        if isinstance(other, pl.Expr):
            return F.lit(self).__mod__(other)
        if self.dtype.is_temporal():
            msg = "first cast to integer before applying modulo on datelike dtypes"
            raise TypeError(msg)
        return self._arithmetic(other, "rem", "rem_<>")
