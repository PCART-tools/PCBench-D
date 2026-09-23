    @cached_property
    def sum(self) -> list[float]:
        """Sum of all pixels for each band in the image."""

        v = []
        for i in range(0, len(self.h), 256):
            layer_sum = 0.0
            for j in range(256):
                layer_sum += j * self.h[i + j]
            v.append(layer_sum)
        return v
