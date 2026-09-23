    def __rpow__(self, other: _Operand | float) -> _Operand:
        return self.apply("pow", other, self)
