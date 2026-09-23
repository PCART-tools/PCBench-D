    def _validate_datetimelike_monotonic(self):
        """
        Validate that each group in self._on is monotonic
        """
        # GH 46061
        if self._on.hasnans:
            self._raise_monotonic_error("values must not have NaT")
        for group_indices in self._grouper.indices.values():
            group_on = self._on.take(group_indices)
            if not (
                group_on.is_monotonic_increasing or group_on.is_monotonic_decreasing
            ):
                on = "index" if self.on is None else self.on
                raise ValueError(
                    f"Each group within {on} must be monotonic. "
                    f"Sort the values in {on} first."
                )
