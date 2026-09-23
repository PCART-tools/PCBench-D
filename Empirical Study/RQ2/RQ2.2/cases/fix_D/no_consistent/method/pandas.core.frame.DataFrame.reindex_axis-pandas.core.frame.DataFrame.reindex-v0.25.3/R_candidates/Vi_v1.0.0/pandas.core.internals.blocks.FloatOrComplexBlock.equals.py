    def equals(self, other) -> bool:
        if self.dtype != other.dtype or self.shape != other.shape:
            return False
        left, right = self.values, other.values
        return ((left == right) | (np.isnan(left) & np.isnan(right))).all()
