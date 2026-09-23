    def load(
        self, dpi: float | tuple[float, float] | None = None
    ) -> Image.core.PixelAccess | None:
        if dpi is not None:
            self.info["dpi"] = dpi
            x0, y0, x1, y1 = self.info["wmf_bbox"]
            if not isinstance(dpi, tuple):
                dpi = dpi, dpi
            self._size = (
                int((x1 - x0) * dpi[0] / self._inch[0]),
                int((y1 - y0) * dpi[1] / self._inch[1]),
            )
        return super().load()
