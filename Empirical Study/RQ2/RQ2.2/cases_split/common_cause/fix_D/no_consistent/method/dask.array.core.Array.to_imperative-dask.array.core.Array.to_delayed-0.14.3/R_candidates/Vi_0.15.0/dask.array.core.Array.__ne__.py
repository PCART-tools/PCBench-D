    def __ne__(self, other):
        return elemwise(operator.ne, self, other)
