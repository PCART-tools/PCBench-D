    @cache_readonly
    def is_monotonic_increasing(self):
        return self._range.step > 0 or len(self) <= 1
