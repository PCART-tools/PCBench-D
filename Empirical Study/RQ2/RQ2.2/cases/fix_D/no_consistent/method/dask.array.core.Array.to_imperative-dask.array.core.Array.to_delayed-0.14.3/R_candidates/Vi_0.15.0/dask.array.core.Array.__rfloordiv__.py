    def __rfloordiv__(self, other):
        return elemwise(operator.floordiv, other, self)
