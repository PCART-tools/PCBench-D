    def chord(
        self,
        xy: Coords,
        start: float,
        end: float,
        fill: _Ink | None = None,
        outline: _Ink | None = None,
        width: int = 1,
    ) -> None:
        """Draw a chord."""
        ink, fill_ink = self._getink(outline, fill)
        if fill_ink is not None:
            self.draw.draw_chord(xy, start, end, fill_ink, 1)
        if ink is not None and ink != fill_ink and width != 0:
            self.draw.draw_chord(xy, start, end, ink, 0, width)
