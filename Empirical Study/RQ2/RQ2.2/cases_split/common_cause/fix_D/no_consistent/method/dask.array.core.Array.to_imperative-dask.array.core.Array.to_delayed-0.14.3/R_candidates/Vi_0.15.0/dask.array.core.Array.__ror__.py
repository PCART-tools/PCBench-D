    def __ror__(self, other):
        return elemwise(operator.or_, other, self)
