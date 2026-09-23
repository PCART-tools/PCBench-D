    def _intersection_via_get_indexer(self, other: Index, sort) -> ArrayLike:
        """
        Find the intersection of two Indexes using get_indexer.

        Returns
        -------
        np.ndarray or ExtensionArray
            The returned array will be unique.
        """
        left_unique = self.unique()
        right_unique = other.unique()

        # even though we are unique, we need get_indexer_for for IntervalIndex
        indexer = left_unique.get_indexer_for(right_unique)

        mask = indexer != -1

        taker = indexer.take(mask.nonzero()[0])
        if sort is False:
            # sort bc we want the elements in the same order they are in self
            # unnecessary in the case with sort=None bc we will sort later
            taker = np.sort(taker)

        result = left_unique.take(taker)._values
        return result
