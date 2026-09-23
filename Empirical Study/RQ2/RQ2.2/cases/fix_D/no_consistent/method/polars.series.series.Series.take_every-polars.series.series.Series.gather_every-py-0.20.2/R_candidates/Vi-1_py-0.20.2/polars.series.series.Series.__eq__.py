    def __eq__(self, other: Any) -> Series | Expr:
        _warn_null_comparison(other)
        if isinstance(other, pl.Expr):
            return F.lit(self).__eq__(other)
        return self._comp(other, "eq")
