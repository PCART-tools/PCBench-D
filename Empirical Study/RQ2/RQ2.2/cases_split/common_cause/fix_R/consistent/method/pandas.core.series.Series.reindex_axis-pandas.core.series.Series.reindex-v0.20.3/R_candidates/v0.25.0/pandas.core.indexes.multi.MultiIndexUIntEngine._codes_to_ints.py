    def _codes_to_ints(self, codes):
        """
        Transform combination(s) of uint64 in one uint64 (each), in a strictly
        monotonic way (i.e. respecting the lexicographic order of integer
        combinations): see BaseMultiIndexCodesEngine documentation.

        Parameters
        ----------
        codes : 1- or 2-dimensional array of dtype uint64
            Combinations of integers (one per row)

        Returns
        -------
        int_keys : scalar or 1-dimensional array, of dtype uint64
            Integer(s) representing one combination (each).
        """
        # Shift the representation of each level by the pre-calculated number
        # of bits:
        codes <<= self.offsets

        # Now sum and OR are in fact interchangeable. This is a simple
        # composition of the (disjunct) significant bits of each level (i.e.
        # each column in "codes") in a single positive integer:
        if codes.ndim == 1:
            # Single key
            return np.bitwise_or.reduce(codes)

        # Multiple keys
        return np.bitwise_or.reduce(codes, axis=1)
