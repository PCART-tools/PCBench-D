    def blit(self, bbox=None):
        # docstring inherited
        if bbox is None and self.figure:
            bbox = self.figure.bbox  # Blit the entire canvas if bbox is None.
        # repaint uses logical pixels, not physical pixels like the renderer.
        l, b, w, h = [int(pt / self._dpi_ratio) for pt in bbox.bounds]
        t = b + h
        self.repaint(l, self.rect().height() - t, w, h)
