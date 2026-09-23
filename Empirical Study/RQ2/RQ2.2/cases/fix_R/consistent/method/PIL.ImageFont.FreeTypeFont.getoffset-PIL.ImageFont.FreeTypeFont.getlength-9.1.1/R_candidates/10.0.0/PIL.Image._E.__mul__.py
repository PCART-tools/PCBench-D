    def __mul__(self, other):
        if isinstance(other, _E):
            return NotImplemented
        return _E(self.scale * other, self.offset * other)
