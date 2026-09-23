    def __ne__(self, other: _Operand | float) -> _Operand:  # type: ignore[override]
        return self.apply("ne", self, other)
