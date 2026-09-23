    @cache_readonly
    def is_monotonic_decreasing(self) -> bool:
        """
        Return a boolean if the values are equal or decreasing.
        """
        # monotonic decreasing if and only if reverse is monotonic increasing
        return self[::-1].is_monotonic_increasing
