    def __le__(self, other):
        return elemwise(operator.le, self, other)
