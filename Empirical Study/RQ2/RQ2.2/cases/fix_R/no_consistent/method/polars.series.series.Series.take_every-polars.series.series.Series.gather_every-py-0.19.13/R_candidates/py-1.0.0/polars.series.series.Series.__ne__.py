    def __ne__(self, other: Any) -> Series | Expr:
        warn_null_comparison(other)
        if isinstance(other, pl.Expr):
            return F.lit(self).__ne__(other)
        return self._comp(other, "neq")
