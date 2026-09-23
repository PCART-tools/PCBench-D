    def __add__(self, other):
        return elemwise(operator.add, self, other)
