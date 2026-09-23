    def __gt__(self, other: _Operand | float) -> _Operand:
        return self.apply("gt", self, other)
