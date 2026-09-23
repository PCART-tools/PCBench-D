    def __lt__(self, other: _Operand | float) -> _Operand:
        return self.apply("lt", self, other)
