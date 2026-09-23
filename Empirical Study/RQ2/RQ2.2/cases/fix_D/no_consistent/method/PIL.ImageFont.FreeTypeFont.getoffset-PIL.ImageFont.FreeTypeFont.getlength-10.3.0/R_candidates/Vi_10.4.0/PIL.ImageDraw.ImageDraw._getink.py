    def _getink(
        self, ink: _Ink | None, fill: _Ink | None = None
    ) -> tuple[int | None, int | None]:
        result_ink = None
        result_fill = None
        if ink is None and fill is None:
            if self.fill:
                result_fill = self.ink
            else:
                result_ink = self.ink
        else:
            if ink is not None:
                if isinstance(ink, str):
                    ink = ImageColor.getcolor(ink, self.mode)
                if self.palette and not isinstance(ink, numbers.Number):
                    ink = self.palette.getcolor(ink, self._image)
                result_ink = self.draw.draw_ink(ink)
            if fill is not None:
                if isinstance(fill, str):
                    fill = ImageColor.getcolor(fill, self.mode)
                if self.palette and not isinstance(fill, numbers.Number):
                    fill = self.palette.getcolor(fill, self._image)
                result_fill = self.draw.draw_ink(fill)
        return result_ink, result_fill
