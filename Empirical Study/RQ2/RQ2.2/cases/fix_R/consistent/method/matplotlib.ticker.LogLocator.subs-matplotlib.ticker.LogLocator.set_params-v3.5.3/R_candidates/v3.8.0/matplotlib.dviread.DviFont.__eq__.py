    def __eq__(self, other):
        return (type(self) is type(other)
                and self.texname == other.texname and self.size == other.size)
