    def __add__(self, other: _Operand | float) -> _Operand:
        return self.apply("add", self, other)
