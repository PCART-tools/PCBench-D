    def __sub__(self, other: Any) -> Self | Expr:
        if isinstance(other, pl.Expr):
            return F.lit(self) - other
        return self._arithmetic(other, "sub", "sub_<>")
