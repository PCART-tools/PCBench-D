    @property
    def is_monotonic_decreasing(self):
        return Index(self.codes).is_monotonic_decreasing
