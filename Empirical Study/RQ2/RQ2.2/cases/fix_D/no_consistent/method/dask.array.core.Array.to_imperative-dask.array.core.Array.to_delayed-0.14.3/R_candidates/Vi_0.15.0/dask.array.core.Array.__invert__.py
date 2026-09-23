    def __invert__(self):
        return elemwise(operator.invert, self)
