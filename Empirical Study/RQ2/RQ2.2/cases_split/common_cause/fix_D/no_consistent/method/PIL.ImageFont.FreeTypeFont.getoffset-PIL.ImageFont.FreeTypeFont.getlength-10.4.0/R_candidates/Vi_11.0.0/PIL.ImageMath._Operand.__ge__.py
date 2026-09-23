    def __ge__(self, other: _Operand | float) -> _Operand:
        return self.apply("ge", self, other)
