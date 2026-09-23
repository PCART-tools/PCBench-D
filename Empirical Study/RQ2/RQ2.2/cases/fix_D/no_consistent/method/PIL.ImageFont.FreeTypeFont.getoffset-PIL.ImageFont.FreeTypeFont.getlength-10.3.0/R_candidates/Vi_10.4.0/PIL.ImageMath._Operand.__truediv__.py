    def __truediv__(self, other: _Operand | float) -> _Operand:
        return self.apply("div", self, other)
