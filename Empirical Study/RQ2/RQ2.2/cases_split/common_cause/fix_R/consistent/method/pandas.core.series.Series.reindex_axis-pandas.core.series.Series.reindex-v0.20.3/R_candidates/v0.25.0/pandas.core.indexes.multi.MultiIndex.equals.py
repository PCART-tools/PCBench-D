    def equals(self, other):
        """
        Determines if two MultiIndex objects have the same labeling information
        (the levels themselves do not necessarily have to be the same)

        See Also
        --------
        equal_levels
        """
        if self.is_(other):
            return True

        if not isinstance(other, Index):
            return False

        if not isinstance(other, MultiIndex):
            other_vals = com.values_from_object(ensure_index(other))
            return array_equivalent(self._ndarray_values, other_vals)

        if self.nlevels != other.nlevels:
            return False

        if len(self) != len(other):
            return False

        for i in range(self.nlevels):
            self_codes = self.codes[i]
            self_codes = self_codes[self_codes != -1]
            self_values = algos.take_nd(
                np.asarray(self.levels[i]._values), self_codes, allow_fill=False
            )

            other_codes = other.codes[i]
            other_codes = other_codes[other_codes != -1]
            other_values = algos.take_nd(
                np.asarray(other.levels[i]._values), other_codes, allow_fill=False
            )

            # since we use NaT both datetime64 and timedelta64
            # we can have a situation where a level is typed say
            # timedelta64 in self (IOW it has other values than NaT)
            # but types datetime64 in other (where its all NaT)
            # but these are equivalent
            if len(self_values) == 0 and len(other_values) == 0:
                continue

            if not array_equivalent(self_values, other_values):
                return False

        return True
