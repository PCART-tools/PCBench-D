    def __rmod__(self, other: _Operand | float) -> _Operand:
        return self.apply("mod", other, self)
