    def __le__(self, other: Any) -> Series | Expr:
        _warn_null_comparison(other)
        if isinstance(other, pl.Expr):
            return F.lit(self).__le__(other)
        return self._comp(other, "lt_eq")
