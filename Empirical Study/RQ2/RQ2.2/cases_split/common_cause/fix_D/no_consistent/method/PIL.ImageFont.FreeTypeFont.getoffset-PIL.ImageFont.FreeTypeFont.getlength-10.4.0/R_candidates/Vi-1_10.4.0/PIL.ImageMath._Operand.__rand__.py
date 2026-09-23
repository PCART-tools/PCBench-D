    def __rand__(self, other: _Operand | float) -> _Operand:
        return self.apply("and", other, self)
