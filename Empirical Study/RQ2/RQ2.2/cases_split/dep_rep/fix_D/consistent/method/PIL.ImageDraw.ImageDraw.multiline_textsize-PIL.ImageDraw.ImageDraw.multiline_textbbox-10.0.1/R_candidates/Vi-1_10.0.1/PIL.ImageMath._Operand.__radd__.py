    def __radd__(self, other):
        return self.apply("add", other, self)
