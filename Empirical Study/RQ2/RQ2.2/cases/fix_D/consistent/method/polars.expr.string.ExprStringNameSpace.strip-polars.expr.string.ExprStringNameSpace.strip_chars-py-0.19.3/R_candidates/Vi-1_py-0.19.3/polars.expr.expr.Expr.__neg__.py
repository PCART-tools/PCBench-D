    def __neg__(self) -> Expr:
        return F.lit(0) - self
