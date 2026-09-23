    @cached_property
    def mean(self) -> list[float]:
        """Average (arithmetic mean) pixel level for each band in the image."""
        return [self.sum[i] / self.count[i] for i in self.bands]
