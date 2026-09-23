    @property
    def is_monotonic_decreasing(self):
        """
        return if the index is monotonic decreasing (only equal or
        decreasing) values.
        """
        return self._engine.is_monotonic_decreasing
