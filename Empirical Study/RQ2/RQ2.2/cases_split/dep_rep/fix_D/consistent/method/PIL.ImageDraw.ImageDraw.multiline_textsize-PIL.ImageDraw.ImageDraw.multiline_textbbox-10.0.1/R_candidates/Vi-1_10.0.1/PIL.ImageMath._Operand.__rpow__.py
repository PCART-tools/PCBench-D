    def __rpow__(self, other):
        return self.apply("pow", other, self)
