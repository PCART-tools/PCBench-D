    def bitmap(
        self, xy: Sequence[int], bitmap: Image.Image, fill: _Ink | None = None
    ) -> None:
        """Draw a bitmap."""
        bitmap.load()
        ink, fill = self._getink(fill)
        if ink is None:
            ink = fill
        if ink is not None:
            self.draw.draw_bitmap(xy, bitmap.im, ink)
