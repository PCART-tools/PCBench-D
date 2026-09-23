    def __rsub__(self, other):
        return self.apply("sub", other, self)
