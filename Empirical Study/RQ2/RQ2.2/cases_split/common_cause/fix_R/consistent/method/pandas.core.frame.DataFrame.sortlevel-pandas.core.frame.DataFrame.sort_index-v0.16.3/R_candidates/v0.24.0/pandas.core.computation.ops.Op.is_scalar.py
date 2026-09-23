    @property
    def is_scalar(self):
        return all(operand.is_scalar for operand in self.operands)
