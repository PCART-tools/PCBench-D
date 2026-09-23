    def __pow__(self, exponent: int | float | None | Series) -> Series:
        return self.pow(exponent)
