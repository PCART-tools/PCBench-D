    def __rand__(self, other):
        return elemwise(operator.and_, other, self)
