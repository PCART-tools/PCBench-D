    def __rand__(self, other):
        return self.apply("and", other, self)
