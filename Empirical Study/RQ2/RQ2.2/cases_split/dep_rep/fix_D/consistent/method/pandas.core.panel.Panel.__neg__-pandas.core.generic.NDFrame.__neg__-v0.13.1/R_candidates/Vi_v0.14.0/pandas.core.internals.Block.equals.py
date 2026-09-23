    def equals(self, other):
        if self.dtype != other.dtype or self.shape != other.shape: return False
        return np.array_equal(self.values, other.values)
