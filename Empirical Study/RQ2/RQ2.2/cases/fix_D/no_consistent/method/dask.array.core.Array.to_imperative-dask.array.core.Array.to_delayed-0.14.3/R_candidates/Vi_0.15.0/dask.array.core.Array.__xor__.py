    def __xor__(self, other):
        return elemwise(operator.xor, self, other)
