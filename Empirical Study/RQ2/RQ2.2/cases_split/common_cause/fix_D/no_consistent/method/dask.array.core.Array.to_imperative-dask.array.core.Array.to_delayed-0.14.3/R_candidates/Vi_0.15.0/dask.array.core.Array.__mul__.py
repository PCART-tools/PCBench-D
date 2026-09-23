    def __mul__(self, other):
        return elemwise(operator.mul, self, other)
