    @property
    def is_monotonic_increasing(self):
        """
        return if the index is monotonic increasing (only equal or
        increasing) values.
        """
        return self._engine.is_monotonic_increasing
