    def __rshift__(self, other):
        return elemwise(operator.rshift, self, other)
