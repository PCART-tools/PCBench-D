    @cache_readonly
    def is_non_overlapping_monotonic(self):
        """
        Return True if the IntervalIndex is non-overlapping (no Intervals share
        points) and is either monotonic increasing or monotonic decreasing,
        else False
        """
        # must be increasing  (e.g., [0, 1), [1, 2), [2, 3), ... )
        # or decreasing (e.g., [-1, 0), [-2, -1), [-3, -2), ...)
        # we already require left <= right

        # strict inequality for closed == 'both'; equality implies overlapping
        # at a point when both sides of intervals are included
        if self.closed == 'both':
            return bool((self.right[:-1] < self.left[1:]).all() or
                        (self.left[:-1] > self.right[1:]).all())

        # non-strict inequality when closed != 'both'; at least one side is
        # not included in the intervals, so equality does not imply overlapping
        return bool((self.right[:-1] <= self.left[1:]).all() or
                    (self.left[:-1] >= self.right[1:]).all())
