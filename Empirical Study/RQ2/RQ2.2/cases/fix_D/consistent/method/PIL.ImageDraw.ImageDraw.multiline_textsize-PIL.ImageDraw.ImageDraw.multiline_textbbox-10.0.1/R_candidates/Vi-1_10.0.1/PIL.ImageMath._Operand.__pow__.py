    def __pow__(self, other):
        return self.apply("pow", self, other)
