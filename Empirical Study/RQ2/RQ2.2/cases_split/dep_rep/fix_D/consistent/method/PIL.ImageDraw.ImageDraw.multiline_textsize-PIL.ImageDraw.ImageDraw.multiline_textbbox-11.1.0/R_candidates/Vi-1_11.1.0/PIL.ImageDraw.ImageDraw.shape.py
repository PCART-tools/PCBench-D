    def shape(
        self,
        shape: Image.core._Outline,
        fill: _Ink | None = None,
        outline: _Ink | None = None,
    ) -> None:
        """(Experimental) Draw a shape."""
        shape.close()
        ink, fill_ink = self._getink(outline, fill)
        if fill_ink is not None:
            self.draw.draw_outline(shape, fill_ink, 1)
        if ink is not None and ink != fill_ink:
            self.draw.draw_outline(shape, ink, 0)
