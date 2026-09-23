    def __and__(self, other: _Operand | float) -> _Operand:
        return self.apply("and", self, other)
