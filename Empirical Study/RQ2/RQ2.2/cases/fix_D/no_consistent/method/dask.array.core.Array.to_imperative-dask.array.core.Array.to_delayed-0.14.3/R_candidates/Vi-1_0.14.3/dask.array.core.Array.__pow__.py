    def __pow__(self, other):
        return elemwise(operator.pow, self, other)
