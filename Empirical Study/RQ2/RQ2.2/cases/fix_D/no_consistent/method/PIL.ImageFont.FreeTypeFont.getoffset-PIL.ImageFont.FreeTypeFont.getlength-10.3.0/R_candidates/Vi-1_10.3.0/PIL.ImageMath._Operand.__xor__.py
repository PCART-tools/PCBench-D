    def __xor__(self, other: _Operand | float) -> _Operand:
        return self.apply("xor", self, other)
