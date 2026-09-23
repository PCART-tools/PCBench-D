    def __eq__(self, other: _Operand | float) -> _Operand:  # type: ignore[override]
        return self.apply("eq", self, other)
