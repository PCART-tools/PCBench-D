    def __rshift__(self, other: _Operand | float) -> _Operand:
        return self.apply("rshift", self, other)
