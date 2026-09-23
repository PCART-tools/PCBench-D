    def __ror__(self, other: _Operand | float) -> _Operand:
        return self.apply("or", other, self)
