    def __floordiv__(self, other):
        return elemwise(operator.floordiv, self, other)
