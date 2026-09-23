    def __rxor__(self, other):
        return elemwise(operator.xor, other, self)
