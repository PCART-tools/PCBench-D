    def __lshift__(self, other: _Operand | float) -> _Operand:
        return self.apply("lshift", self, other)
