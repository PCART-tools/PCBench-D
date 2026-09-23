    def __abs__(self) -> _Operand:
        return self.apply("abs", self)
