    def equals(self, other):
        """
        Determines if two Index objects contain the same elements.
        """
        if self.is_(other):
            return True

        if not isinstance(other, Index):
            return False

        if type(other) != Index:
            return other.equals(self)

        return np.array_equal(self, other)
