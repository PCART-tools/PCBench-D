    def __add__(self, other: Any) -> Self | DataFrame | Expr:
        if isinstance(other, str):
            other = Series("", [other])
        elif isinstance(other, pl.DataFrame):
            return other + self
        elif isinstance(other, pl.Expr):
            return F.lit(self) + other
        return self._arithmetic(other, "add", "add_<>")
