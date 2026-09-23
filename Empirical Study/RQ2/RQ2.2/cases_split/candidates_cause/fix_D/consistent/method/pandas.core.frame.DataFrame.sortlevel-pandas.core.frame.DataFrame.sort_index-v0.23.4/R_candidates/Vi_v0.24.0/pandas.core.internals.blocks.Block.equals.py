    def equals(self, other):
        if self.dtype != other.dtype or self.shape != other.shape:
            return False
        return array_equivalent(self.values, other.values)
