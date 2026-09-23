    @cached_property
    def var(self) -> list[float]:
        """Variance for each band in the image."""
        return [
            (self.sum2[i] - (self.sum[i] ** 2.0) / self.count[i]) / self.count[i]
            for i in self.bands
        ]
