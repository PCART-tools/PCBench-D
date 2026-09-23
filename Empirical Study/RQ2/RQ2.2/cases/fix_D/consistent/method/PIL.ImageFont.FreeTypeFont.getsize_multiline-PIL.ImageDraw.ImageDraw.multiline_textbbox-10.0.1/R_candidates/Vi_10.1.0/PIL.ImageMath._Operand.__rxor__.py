    def __rxor__(self, other):
        return self.apply("xor", other, self)
