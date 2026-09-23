    def __pow__(self, power: int | float | Series | Expr) -> Self:
        return self.pow(power)
