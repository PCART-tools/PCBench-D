    def __eq__(self, other):
        return isinstance(other, Name) and self.name == other.name
