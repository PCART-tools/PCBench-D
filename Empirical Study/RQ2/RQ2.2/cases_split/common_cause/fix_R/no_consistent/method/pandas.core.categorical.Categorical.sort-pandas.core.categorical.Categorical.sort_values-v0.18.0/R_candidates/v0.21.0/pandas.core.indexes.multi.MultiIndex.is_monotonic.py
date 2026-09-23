    @cache_readonly
    def is_monotonic(self):
        """
        return if the index is monotonic increasing (only equal or
        increasing) values.
        """
        return self.is_monotonic_increasing
