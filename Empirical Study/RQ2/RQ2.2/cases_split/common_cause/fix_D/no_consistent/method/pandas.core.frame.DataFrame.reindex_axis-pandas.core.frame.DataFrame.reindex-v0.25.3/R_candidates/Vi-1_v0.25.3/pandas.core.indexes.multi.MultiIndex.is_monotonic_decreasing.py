    @cache_readonly
    def is_monotonic_decreasing(self):
        """
        return if the index is monotonic decreasing (only equal or
        decreasing) values.
        """
        # monotonic decreasing if and only if reverse is monotonic increasing
        return self[::-1].is_monotonic_increasing
