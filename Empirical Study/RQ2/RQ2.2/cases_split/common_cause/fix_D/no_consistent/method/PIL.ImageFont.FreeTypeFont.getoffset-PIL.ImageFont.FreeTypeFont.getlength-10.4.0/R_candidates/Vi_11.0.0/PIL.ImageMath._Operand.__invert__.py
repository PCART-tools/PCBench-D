    def __invert__(self) -> _Operand:
        return self.apply("invert", self)
