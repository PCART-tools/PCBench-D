    def __gt__(self, other):
        return elemwise(operator.gt, self, other)
