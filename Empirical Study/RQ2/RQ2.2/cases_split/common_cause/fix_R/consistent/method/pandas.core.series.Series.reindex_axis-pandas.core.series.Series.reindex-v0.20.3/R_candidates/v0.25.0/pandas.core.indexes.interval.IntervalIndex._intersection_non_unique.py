    def _intersection_non_unique(self, other: "IntervalIndex") -> "IntervalIndex":
        """
        Used when the IntervalIndex does have some common endpoints,
        on either sides.
        Return the intersection with another IntervalIndex.

        Parameters
        ----------
        other : IntervalIndex

        Returns
        -------
        taken : IntervalIndex
        """
        mask = np.zeros(len(self), dtype=bool)

        if self.hasnans and other.hasnans:
            first_nan_loc = np.arange(len(self))[self.isna()][0]
            mask[first_nan_loc] = True

        lmiss = other.left.get_indexer_non_unique(self.left)[1]
        lmatch = np.setdiff1d(np.arange(len(self)), lmiss)

        for i in lmatch:
            potential = other.left.get_loc(self.left[i])
            if is_scalar(potential):
                if self.right[i] == other.right[potential]:
                    mask[i] = True
            elif self.right[i] in other.right[potential]:
                mask[i] = True

        return self[mask]
