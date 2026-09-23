    def __truediv__(self, other):
        return elemwise(operator.truediv, self, other)
