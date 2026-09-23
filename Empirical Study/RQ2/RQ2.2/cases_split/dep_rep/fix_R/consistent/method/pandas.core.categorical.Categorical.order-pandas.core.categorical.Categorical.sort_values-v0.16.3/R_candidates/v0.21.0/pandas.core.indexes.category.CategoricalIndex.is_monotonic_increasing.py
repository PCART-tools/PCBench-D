    @property
    def is_monotonic_increasing(self):
        return Index(self.codes).is_monotonic_increasing
