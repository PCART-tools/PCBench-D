    def _get_fill_indexer_searchsorted(self, target, method, limit=None):
        """
        Fallback pad/backfill get_indexer that works for monotonic decreasing
        indexes and non-monotonic targets.
        """
        if limit is not None:
            raise ValueError('limit argument for %r method only well-defined '
                             'if index and target are monotonic' % method)

        side = 'left' if method == 'pad' else 'right'

        # find exact matches first (this simplifies the algorithm)
        indexer = self.get_indexer(target)
        nonexact = (indexer == -1)
        indexer[nonexact] = self._searchsorted_monotonic(target[nonexact],
                                                         side)
        if side == 'left':
            # searchsorted returns "indices into a sorted array such that,
            # if the corresponding elements in v were inserted before the
            # indices, the order of a would be preserved".
            # Thus, we need to subtract 1 to find values to the left.
            indexer[nonexact] -= 1
            # This also mapped not found values (values of 0 from
            # np.searchsorted) to -1, which conveniently is also our
            # sentinel for missing values
        else:
            # Mark indices to the right of the largest value as not found
            indexer[indexer == len(self)] = -1
        return indexer
