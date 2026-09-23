    def __rmul__(self, other):
        return self.apply("mul", other, self)
