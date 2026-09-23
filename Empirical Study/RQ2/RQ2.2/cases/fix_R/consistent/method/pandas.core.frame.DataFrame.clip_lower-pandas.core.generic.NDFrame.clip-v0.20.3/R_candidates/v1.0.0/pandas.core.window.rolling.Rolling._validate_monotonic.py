    def _validate_monotonic(self):
        """
        Validate monotonic (increasing or decreasing).
        """
        if not (self._on.is_monotonic_increasing or self._on.is_monotonic_decreasing):
            formatted = self.on
            if self.on is None:
                formatted = "index"
            raise ValueError(f"{formatted} must be monotonic")
