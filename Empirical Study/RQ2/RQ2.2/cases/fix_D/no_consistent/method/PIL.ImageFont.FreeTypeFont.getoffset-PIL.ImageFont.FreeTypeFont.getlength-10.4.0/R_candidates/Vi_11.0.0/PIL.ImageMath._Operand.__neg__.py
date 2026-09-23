    def __neg__(self) -> _Operand:
        return self.apply("neg", self)
