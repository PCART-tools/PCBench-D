    def __rmod__(self, other):
        return elemwise(operator.mod, other, self)
