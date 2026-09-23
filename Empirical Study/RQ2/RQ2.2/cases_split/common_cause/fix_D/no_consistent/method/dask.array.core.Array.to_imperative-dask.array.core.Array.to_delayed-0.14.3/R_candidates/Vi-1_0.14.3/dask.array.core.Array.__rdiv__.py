    def __rdiv__(self, other):
        return elemwise(operator.div, other, self)
