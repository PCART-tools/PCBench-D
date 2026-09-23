    def equals(self, other):
        """
        Determines if two Index objects contain the same elements.
        """
        if self is other:
            return True

        try:
            return np.array_equal(self, other)
        except TypeError:
            # e.g. fails in numpy 1.6 with DatetimeIndex #1681
            return False
