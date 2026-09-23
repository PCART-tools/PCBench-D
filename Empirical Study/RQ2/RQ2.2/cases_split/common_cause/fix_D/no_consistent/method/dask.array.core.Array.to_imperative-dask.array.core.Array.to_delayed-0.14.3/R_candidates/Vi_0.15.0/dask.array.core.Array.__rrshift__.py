    def __rrshift__(self, other):
        return elemwise(operator.rshift, other, self)
