    def _check_compatible_with(self, other) -> None:
        if other is NaT:
            return
        self._require_matching_freq(other)
