    def __ror__(self, other):
        return self.apply("or", other, self)
