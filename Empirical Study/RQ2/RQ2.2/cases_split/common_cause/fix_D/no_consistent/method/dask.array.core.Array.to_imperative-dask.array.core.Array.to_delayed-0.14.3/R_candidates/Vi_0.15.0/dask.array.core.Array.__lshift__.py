    def __lshift__(self, other):
        return elemwise(operator.lshift, self, other)
