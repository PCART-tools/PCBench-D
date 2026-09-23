    def textbbox(
        self,
        xy: tuple[float, float],
        text: AnyStr,
        font: (
            ImageFont.ImageFont
            | ImageFont.FreeTypeFont
            | ImageFont.TransposedFont
            | None
        ) = None,
        anchor: str | None = None,
        spacing: float = 4,
        align: str = "left",
        direction: str | None = None,
        features: list[str] | None = None,
        language: str | None = None,
        stroke_width: float = 0,
        embedded_color: bool = False,
        *,
        font_size: float | None = None,
    ) -> tuple[float, float, float, float]:
        """Get the bounding box of a given string, in pixels."""
        if embedded_color and self.mode not in ("RGB", "RGBA"):
            msg = "Embedded color supported only in RGB and RGBA modes"
            raise ValueError(msg)

        if font is None:
            font = self._getfont(font_size)

        if self._multiline_check(text):
            return self.multiline_textbbox(
                xy,
                text,
                font,
                anchor,
                spacing,
                align,
                direction,
                features,
                language,
                stroke_width,
                embedded_color,
            )

        mode = "RGBA" if embedded_color else self.fontmode
        bbox = font.getbbox(
            text, mode, direction, features, language, stroke_width, anchor
        )
        return bbox[0] + xy[0], bbox[1] + xy[1], bbox[2] + xy[0], bbox[3] + xy[1]
