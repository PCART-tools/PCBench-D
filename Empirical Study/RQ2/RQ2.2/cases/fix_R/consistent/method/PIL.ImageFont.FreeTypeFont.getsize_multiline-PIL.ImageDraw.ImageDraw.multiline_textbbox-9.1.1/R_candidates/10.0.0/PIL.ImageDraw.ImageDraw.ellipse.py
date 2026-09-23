    def ellipse(self, xy, fill=None, outline=None, width=1):
        """Draw an ellipse."""
        ink, fill = self._getink(outline, fill)
        if fill is not None:
            self.draw.draw_ellipse(xy, fill, 1)
        if ink is not None and ink != fill and width != 0:
            self.draw.draw_ellipse(xy, ink, 0, width)
