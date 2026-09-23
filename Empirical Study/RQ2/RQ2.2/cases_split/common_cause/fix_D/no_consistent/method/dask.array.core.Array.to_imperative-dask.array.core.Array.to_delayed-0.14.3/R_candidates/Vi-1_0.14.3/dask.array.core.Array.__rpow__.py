    def __rpow__(self, other):
        return elemwise(operator.pow, other, self)
