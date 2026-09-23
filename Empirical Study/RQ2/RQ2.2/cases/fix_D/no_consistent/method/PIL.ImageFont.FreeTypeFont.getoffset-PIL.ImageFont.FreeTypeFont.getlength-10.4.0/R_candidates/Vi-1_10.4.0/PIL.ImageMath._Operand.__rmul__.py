    def __rmul__(self, other: _Operand | float) -> _Operand:
        return self.apply("mul", other, self)
