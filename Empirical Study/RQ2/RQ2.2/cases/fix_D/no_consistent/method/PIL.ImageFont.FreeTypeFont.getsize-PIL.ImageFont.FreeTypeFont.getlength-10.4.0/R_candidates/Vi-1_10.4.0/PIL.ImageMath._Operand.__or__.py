    def __or__(self, other: _Operand | float) -> _Operand:
        return self.apply("or", self, other)
