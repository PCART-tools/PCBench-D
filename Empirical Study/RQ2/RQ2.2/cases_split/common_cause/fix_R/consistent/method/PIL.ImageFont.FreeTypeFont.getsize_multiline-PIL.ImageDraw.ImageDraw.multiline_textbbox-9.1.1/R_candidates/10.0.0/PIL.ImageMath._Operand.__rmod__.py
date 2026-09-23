    def __rmod__(self, other):
        return self.apply("mod", other, self)
