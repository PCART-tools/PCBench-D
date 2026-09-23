    @cached_property
    def count(self) -> list[int]:
        """Total number of pixels for each band in the image."""
        return [sum(self.h[i : i + 256]) for i in range(0, len(self.h), 256)]
