    def __pos__(self) -> Expr:
        return F.lit(0) + self
