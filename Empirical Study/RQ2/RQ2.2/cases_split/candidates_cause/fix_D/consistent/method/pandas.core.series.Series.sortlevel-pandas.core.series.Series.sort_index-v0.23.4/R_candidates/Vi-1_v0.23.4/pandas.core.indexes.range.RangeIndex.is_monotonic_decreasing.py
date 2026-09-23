    @cache_readonly
    def is_monotonic_decreasing(self):
        return self._step < 0 or len(self) <= 1
