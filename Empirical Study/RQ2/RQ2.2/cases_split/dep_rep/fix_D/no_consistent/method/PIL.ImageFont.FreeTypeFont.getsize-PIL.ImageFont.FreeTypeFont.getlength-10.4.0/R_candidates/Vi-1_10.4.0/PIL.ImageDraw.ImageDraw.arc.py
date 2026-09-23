    def arc(
        self,
        xy: Coords,
        start: float,
        end: float,
        fill: _Ink | None = None,
        width: int = 1,
    ) -> None:
        """Draw an arc."""
        ink, fill = self._getink(fill)
        if ink is not None:
            self.draw.draw_arc(xy, start, end, ink, width)
