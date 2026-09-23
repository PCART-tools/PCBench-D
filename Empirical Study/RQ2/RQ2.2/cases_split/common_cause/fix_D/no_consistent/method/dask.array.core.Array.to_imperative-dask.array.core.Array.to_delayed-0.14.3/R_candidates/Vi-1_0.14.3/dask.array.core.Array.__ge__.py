    def __ge__(self, other):
        return elemwise(operator.ge, self, other)
