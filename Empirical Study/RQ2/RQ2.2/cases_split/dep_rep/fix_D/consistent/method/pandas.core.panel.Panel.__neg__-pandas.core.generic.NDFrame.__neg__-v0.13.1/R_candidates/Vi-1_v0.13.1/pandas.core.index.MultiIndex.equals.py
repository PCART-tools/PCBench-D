    def equals(self, other):
        """
        Determines if two MultiIndex objects have the same labeling information
        (the levels themselves do not necessarily have to be the same)

        See also
        --------
        equal_levels
        """
        if self.is_(other):
            return True

        if not isinstance(other, MultiIndex):
            return np.array_equal(self.values, _ensure_index(other))

        if self.nlevels != other.nlevels:
            return False

        if len(self) != len(other):
            return False

        for i in range(self.nlevels):
            svalues = com.take_nd(self.levels[i].values, self.labels[i],
                                  allow_fill=False)
            ovalues = com.take_nd(other.levels[i].values, other.labels[i],
                                  allow_fill=False)
            if not np.array_equal(svalues, ovalues):
                return False

        return True
