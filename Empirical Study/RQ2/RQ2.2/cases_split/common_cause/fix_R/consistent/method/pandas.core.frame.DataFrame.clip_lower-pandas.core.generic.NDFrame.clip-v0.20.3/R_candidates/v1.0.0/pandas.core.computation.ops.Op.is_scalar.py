    @property
    def is_scalar(self) -> bool:
        return all(operand.is_scalar for operand in self.operands)
