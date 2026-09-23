    def __rsub__(self, other):
        return elemwise(operator.sub, other, self)
