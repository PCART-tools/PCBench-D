    def multiline_text(
        self,
        xy: tuple[float, float],
        text: AnyStr,
        fill: _Ink | None = None,
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
        stroke_fill: _Ink | None = None,
        embedded_color: bool = False,
        *,
        font_size: float | None = None,
    ) -> None:
        font, anchor, lines = self._prepare_multiline_text(
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
            font_size,
        )

        for xy, line in lines:
            self.text(
                xy,
                line,
                fill,
                font,
                anchor,
                direction=direction,
                features=features,
                language=language,
                stroke_width=stroke_width,
                stroke_fill=stroke_fill,
                embedded_color=embedded_color,
            )
