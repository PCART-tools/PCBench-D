    def __mod__(self, other: _Operand | float) -> _Operand:
        return self.apply("mod", self, other)
