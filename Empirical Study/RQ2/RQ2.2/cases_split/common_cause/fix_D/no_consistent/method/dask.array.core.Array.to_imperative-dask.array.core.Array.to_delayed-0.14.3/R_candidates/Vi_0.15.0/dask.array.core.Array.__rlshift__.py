    def __rlshift__(self, other):
        return elemwise(operator.lshift, other, self)
