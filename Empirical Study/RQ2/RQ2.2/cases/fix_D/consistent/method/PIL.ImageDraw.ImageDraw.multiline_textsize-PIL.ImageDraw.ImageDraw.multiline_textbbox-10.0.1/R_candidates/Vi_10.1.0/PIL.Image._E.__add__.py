    def __add__(self, other):
        if isinstance(other, _E):
            return _E(self.scale + other.scale, self.offset + other.offset)
        return _E(self.scale, self.offset + other)
