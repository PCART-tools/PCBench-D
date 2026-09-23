    def ellipse(
        self,
        xy: Coords,
        fill: _Ink | None = None,
        outline: _Ink | None = None,
        width: int = 1,
    ) -> None:
        """Draw an ellipse."""
        ink, fill_ink = self._getink(outline, fill)
        if fill_ink is not None:
            self.draw.draw_ellipse(xy, fill_ink, 1)
        if ink is not None and ink != fill_ink and width != 0:
            self.draw.draw_ellipse(xy, ink, 0, width)
