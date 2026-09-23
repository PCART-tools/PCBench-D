    def textlength(
        self,
        text: str,
        font: (
            ImageFont.ImageFont
            | ImageFont.FreeTypeFont
            | ImageFont.TransposedFont
            | None
        ) = None,
        direction=None,
        features=None,
        language=None,
        embedded_color=False,
        *,
        font_size=None,
    ) -> float:
        """Get the length of a given string, in pixels with 1/64 precision."""
        if self._multiline_check(text):
            msg = "can't measure length of multiline text"
            raise ValueError(msg)
        if embedded_color and self.mode not in ("RGB", "RGBA"):
            msg = "Embedded color supported only in RGB and RGBA modes"
            raise ValueError(msg)

        if font is None:
            font = self._getfont(font_size)
        mode = "RGBA" if embedded_color else self.fontmode
        return font.getlength(text, mode, direction, features, language)
