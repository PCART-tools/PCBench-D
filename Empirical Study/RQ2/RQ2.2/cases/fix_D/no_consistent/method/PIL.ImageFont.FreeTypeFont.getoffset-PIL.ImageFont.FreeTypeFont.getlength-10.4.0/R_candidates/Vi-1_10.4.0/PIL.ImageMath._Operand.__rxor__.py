    def __rxor__(self, other: _Operand | float) -> _Operand:
        return self.apply("xor", other, self)
