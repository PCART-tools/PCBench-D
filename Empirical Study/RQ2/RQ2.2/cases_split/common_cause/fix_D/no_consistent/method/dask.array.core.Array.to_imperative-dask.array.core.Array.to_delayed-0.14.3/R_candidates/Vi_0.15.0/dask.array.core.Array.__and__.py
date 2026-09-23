    def __and__(self, other):
        return elemwise(operator.and_, self, other)
