    def __le__(self, other: _Operand | float) -> _Operand:
        return self.apply("le", self, other)
