    def pieslice(
        self, xy: Coords, start, end, fill=None, outline=None, width=1
    ) -> None:
        """Draw a pieslice."""
        ink, fill = self._getink(outline, fill)
        if fill is not None:
            self.draw.draw_pieslice(xy, start, end, fill, 1)
        if ink is not None and ink != fill and width != 0:
            self.draw.draw_pieslice(xy, start, end, ink, 0, width)
