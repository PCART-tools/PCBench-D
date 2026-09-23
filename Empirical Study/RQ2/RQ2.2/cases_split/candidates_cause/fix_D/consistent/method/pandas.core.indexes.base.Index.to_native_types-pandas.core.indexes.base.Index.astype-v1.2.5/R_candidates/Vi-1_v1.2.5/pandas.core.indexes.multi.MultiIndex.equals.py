    def equals(self, other: object) -> bool:
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

        if len(self) != len(other):
            return False

        if not isinstance(other, MultiIndex):
            # d-level MultiIndex can equal d-tuple Index
            if not is_object_dtype(other.dtype):
                # other cannot contain tuples, so cannot match self
                return False
            return array_equivalent(self._values, other._values)

        if self.nlevels != other.nlevels:
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

            # since we use NaT both datetime64 and timedelta64 we can have a
            # situation where a level is typed say timedelta64 in self (IOW it
            # has other values than NaT) but types datetime64 in other (where
            # its all NaT) but these are equivalent
            if len(self_values) == 0 and len(other_values) == 0:
                continue

            if not array_equivalent(self_values, other_values):
                return False

        return True
