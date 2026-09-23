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
            return array_equivalent(self.values,
                                    _values_from_object(_ensure_index(other)))

        if self.nlevels != other.nlevels:
            return False

        if len(self) != len(other):
            return False

        for i in range(self.nlevels):
            svalues = com.take_nd(np.asarray(self.levels[i].values), self.labels[i],
                                  allow_fill=False)
            ovalues = com.take_nd(np.asarray(other.levels[i].values), other.labels[i],
                                  allow_fill=False)
            if not array_equivalent(svalues, ovalues):
                return False

        return True
