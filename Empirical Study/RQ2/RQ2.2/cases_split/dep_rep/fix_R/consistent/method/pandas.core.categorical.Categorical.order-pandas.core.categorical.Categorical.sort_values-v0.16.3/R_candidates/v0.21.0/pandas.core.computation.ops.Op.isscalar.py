    @property
    def isscalar(self):
        return all(operand.isscalar for operand in self.operands)
