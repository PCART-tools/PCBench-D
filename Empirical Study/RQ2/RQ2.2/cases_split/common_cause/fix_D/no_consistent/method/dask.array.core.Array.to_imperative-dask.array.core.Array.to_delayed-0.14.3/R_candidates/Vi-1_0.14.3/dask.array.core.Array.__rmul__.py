    def __rmul__(self, other):
        return elemwise(operator.mul, other, self)
