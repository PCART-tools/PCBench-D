    def __mod__(self, other):
        return elemwise(operator.mod, self, other)
