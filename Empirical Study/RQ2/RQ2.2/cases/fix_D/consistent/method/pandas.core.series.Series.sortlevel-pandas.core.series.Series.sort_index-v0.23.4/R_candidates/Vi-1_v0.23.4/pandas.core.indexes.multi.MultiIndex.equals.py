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

        if not isinstance(other, Index):
            return False

        if not isinstance(other, MultiIndex):
            other_vals = com._values_from_object(_ensure_index(other))
            return array_equivalent(self._ndarray_values, other_vals)

        if self.nlevels != other.nlevels:
            return False

        if len(self) != len(other):
            return False

        for i in range(self.nlevels):
            slabels = self.labels[i]
            slabels = slabels[slabels != -1]
            svalues = algos.take_nd(np.asarray(self.levels[i]._values),
                                    slabels, allow_fill=False)

            olabels = other.labels[i]
            olabels = olabels[olabels != -1]
            ovalues = algos.take_nd(
                np.asarray(other.levels[i]._values),
                olabels, allow_fill=False)

            # since we use NaT both datetime64 and timedelta64
            # we can have a situation where a level is typed say
            # timedelta64 in self (IOW it has other values than NaT)
            # but types datetime64 in other (where its all NaT)
            # but these are equivalent
            if len(svalues) == 0 and len(ovalues) == 0:
                continue

            if not array_equivalent(svalues, ovalues):
                return False

        return True
