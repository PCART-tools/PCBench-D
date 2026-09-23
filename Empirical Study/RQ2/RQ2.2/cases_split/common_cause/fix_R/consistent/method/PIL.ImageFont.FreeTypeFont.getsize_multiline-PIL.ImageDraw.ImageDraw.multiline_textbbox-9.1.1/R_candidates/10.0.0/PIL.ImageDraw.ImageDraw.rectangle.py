    def rectangle(self, xy, fill=None, outline=None, width=1):
        """Draw a rectangle."""
        ink, fill = self._getink(outline, fill)
        if fill is not None:
            self.draw.draw_rectangle(xy, fill, 1)
        if ink is not None and ink != fill and width != 0:
            self.draw.draw_rectangle(xy, ink, 0, width)
