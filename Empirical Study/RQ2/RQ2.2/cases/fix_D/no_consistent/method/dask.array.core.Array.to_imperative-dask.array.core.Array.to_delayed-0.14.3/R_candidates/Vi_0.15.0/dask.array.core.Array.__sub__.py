    def __sub__(self, other):
        return elemwise(operator.sub, self, other)
