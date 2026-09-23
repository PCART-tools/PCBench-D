    def __radd__(self, other: _Operand | float) -> _Operand:
        return self.apply("add", other, self)
