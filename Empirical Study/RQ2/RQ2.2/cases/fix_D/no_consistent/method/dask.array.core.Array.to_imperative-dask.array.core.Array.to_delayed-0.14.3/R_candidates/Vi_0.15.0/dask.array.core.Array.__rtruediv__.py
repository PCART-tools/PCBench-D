    def __rtruediv__(self, other):
        return elemwise(operator.truediv, other, self)
