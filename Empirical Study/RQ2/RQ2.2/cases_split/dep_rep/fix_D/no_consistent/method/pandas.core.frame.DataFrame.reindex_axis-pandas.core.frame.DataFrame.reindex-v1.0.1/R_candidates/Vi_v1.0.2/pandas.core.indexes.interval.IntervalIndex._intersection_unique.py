    def _intersection_unique(self, other: "IntervalIndex") -> "IntervalIndex":
        """
        Used when the IntervalIndex does not have any common endpoint,
        no mater left or right.
        Return the intersection with another IntervalIndex.

        Parameters
        ----------
        other : IntervalIndex

        Returns
        -------
        IntervalIndex
        """
        lindexer = self.left.get_indexer(other.left)
        rindexer = self.right.get_indexer(other.right)

        match = (lindexer == rindexer) & (lindexer != -1)
        indexer = lindexer.take(match.nonzero()[0])

        return self.take(indexer)
