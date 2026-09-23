    def __pow__(self, other: _Operand | float) -> _Operand:
        return self.apply("pow", self, other)
