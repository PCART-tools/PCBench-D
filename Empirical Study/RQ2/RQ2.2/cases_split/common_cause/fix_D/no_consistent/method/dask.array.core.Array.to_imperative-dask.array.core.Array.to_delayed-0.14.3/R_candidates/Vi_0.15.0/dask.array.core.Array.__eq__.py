    def __eq__(self, other):
        return elemwise(operator.eq, self, other)
