    def load(self, dpi=None):
        if dpi is not None and self._inch is not None:
            self.info["dpi"] = dpi
            x0, y0, x1, y1 = self.info["wmf_bbox"]
            self._size = (
                (x1 - x0) * self.info["dpi"] // self._inch,
                (y1 - y0) * self.info["dpi"] // self._inch,
            )
        return super().load()
