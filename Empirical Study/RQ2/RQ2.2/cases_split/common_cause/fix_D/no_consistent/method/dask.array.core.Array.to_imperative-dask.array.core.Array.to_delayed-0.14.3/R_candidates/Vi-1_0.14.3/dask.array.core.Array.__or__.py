    def __or__(self, other):
        return elemwise(operator.or_, self, other)
