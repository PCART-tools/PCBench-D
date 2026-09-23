    @cached_property
    def rms(self) -> list[float]:
        """RMS (root-mean-square) for each band in the image."""
        return [math.sqrt(self.sum2[i] / self.count[i]) for i in self.bands]
