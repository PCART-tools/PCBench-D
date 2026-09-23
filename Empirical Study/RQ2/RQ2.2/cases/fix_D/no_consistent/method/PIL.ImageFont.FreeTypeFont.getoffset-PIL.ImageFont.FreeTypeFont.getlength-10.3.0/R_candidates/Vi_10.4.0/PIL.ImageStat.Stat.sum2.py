    @cached_property
    def sum2(self) -> list[float]:
        """Squared sum of all pixels for each band in the image."""

        v = []
        for i in range(0, len(self.h), 256):
            sum2 = 0.0
            for j in range(256):
                sum2 += (j**2) * float(self.h[i + j])
            v.append(sum2)
        return v
