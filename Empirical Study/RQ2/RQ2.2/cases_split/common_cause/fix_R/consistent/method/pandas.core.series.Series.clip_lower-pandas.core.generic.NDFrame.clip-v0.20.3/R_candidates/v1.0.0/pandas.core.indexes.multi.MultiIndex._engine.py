    @cache_readonly
    def _engine(self):
        # Calculate the number of bits needed to represent labels in each
        # level, as log2 of their sizes (including -1 for NaN):
        sizes = np.ceil(np.log2([len(l) + 1 for l in self.levels]))

        # Sum bit counts, starting from the _right_....
        lev_bits = np.cumsum(sizes[::-1])[::-1]

        # ... in order to obtain offsets such that sorting the combination of
        # shifted codes (one for each level, resulting in a unique integer) is
        # equivalent to sorting lexicographically the codes themselves. Notice
        # that each level needs to be shifted by the number of bits needed to
        # represent the _previous_ ones:
        offsets = np.concatenate([lev_bits[1:], [0]]).astype("uint64")

        # Check the total number of bits needed for our representation:
        if lev_bits[0] > 64:
            # The levels would overflow a 64 bit uint - use Python integers:
            return MultiIndexPyIntEngine(self.levels, self.codes, offsets)
        return MultiIndexUIntEngine(self.levels, self.codes, offsets)
