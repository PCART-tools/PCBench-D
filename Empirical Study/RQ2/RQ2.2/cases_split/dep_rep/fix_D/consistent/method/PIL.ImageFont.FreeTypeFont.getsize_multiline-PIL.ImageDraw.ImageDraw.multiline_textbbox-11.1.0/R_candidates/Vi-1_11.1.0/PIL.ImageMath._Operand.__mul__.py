    def __mul__(self, other: _Operand | float) -> _Operand:
        return self.apply("mul", self, other)
