    def _multiline_spacing(
        self,
        font: ImageFont.ImageFont | ImageFont.FreeTypeFont | ImageFont.TransposedFont,
        spacing: float,
        stroke_width: float,
    ) -> float:
        return (
            self.textbbox((0, 0), "A", font, stroke_width=stroke_width)[3]
            + stroke_width
            + spacing
        )
