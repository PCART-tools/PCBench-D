    def shape(self, shape, fill=None, outline=None) -> None:
        """(Experimental) Draw a shape."""
        shape.close()
        ink, fill = self._getink(outline, fill)
        if fill is not None:
            self.draw.draw_outline(shape, fill, 1)
        if ink is not None and ink != fill:
            self.draw.draw_outline(shape, ink, 0)
