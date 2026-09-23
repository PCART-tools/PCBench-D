    def __mul__(self, other):
        return type(self)(super().__mul__(other))
