    def __div__(self, other):
        return elemwise(operator.div, self, other)
