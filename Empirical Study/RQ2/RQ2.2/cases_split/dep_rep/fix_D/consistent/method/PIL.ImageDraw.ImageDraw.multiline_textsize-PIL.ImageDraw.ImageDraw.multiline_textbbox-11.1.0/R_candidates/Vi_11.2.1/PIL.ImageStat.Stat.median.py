    @cached_property
    def median(self) -> list[int]:
        """Median pixel level for each band in the image."""

        v = []
        for i in self.bands:
            s = 0
            half = self.count[i] // 2
            b = i * 256
            for j in range(256):
                s = s + self.h[b + j]
                if s > half:
                    break
            v.append(j)
        return v
