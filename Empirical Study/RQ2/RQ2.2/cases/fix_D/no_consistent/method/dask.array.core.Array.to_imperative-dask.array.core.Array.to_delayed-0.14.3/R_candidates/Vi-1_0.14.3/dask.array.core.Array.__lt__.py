    def __lt__(self, other):
        return elemwise(operator.lt, self, other)
