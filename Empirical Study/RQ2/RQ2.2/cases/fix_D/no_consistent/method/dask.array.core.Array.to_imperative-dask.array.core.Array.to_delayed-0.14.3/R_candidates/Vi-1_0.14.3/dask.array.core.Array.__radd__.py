    def __radd__(self, other):
        return elemwise(operator.add, other, self)
