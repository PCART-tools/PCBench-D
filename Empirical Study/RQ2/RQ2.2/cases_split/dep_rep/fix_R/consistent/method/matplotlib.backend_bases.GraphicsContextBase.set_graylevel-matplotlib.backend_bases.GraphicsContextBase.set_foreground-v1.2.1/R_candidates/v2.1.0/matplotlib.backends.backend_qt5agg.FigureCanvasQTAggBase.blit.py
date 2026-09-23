    def blit(self, bbox=None):
        """Blit the region in bbox.
        """
        # If bbox is None, blit the entire canvas. Otherwise
        # blit only the area defined by the bbox.
        if bbox is None and self.figure:
            bbox = self.figure.bbox

        self._bbox_queue.append(bbox)

        # repaint uses logical pixels, not physical pixels like the renderer.
        l, b, w, h = [pt / self._dpi_ratio for pt in bbox.bounds]
        t = b + h
        self.repaint(l, self.renderer.height / self._dpi_ratio - t, w, h)
