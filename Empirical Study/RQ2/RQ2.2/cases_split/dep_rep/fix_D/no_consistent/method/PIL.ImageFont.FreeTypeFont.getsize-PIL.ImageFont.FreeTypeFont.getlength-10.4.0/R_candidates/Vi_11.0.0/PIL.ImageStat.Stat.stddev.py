    @cached_property
    def stddev(self) -> list[float]:
        """Standard deviation for each band in the image."""
        return [math.sqrt(self.var[i]) for i in self.bands]
