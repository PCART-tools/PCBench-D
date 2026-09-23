    def __sub__(self, other: _Operand | float) -> _Operand:
        return self.apply("sub", self, other)
