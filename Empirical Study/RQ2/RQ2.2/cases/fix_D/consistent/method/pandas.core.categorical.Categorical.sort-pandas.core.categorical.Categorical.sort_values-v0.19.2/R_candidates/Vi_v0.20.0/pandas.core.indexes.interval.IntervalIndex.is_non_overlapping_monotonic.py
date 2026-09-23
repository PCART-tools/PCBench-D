    @cache_readonly
    def is_non_overlapping_monotonic(self):
        # must be increasing  (e.g., [0, 1), [1, 2), [2, 3), ... )
        # or decreasing (e.g., [-1, 0), [-2, -1), [-3, -2), ...)
        # we already require left <= right
        return ((self.right[:-1] <= self.left[1:]).all() or
                (self.left[:-1] >= self.right[1:]).all())
