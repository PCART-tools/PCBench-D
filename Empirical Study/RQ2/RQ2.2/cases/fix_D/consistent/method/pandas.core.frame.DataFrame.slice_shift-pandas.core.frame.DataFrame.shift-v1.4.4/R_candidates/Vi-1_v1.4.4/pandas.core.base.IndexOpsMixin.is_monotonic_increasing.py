    @property
    def is_monotonic_increasing(self) -> bool:
        """
        Alias for is_monotonic.
        """
        # mypy complains if we alias directly
        return self.is_monotonic
