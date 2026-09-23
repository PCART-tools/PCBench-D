    def multiline_textsize(
        self,
        text,
        font=None,
        spacing=4,
        direction=None,
        features=None,
        language=None,
        stroke_width=0,
    ):
        max_width = 0
        lines = self._multiline_split(text)
        line_spacing = (
            self.textsize("A", font=font, stroke_width=stroke_width)[1] + spacing
        )
        for line in lines:
            line_width, line_height = self.textsize(
                line, font, spacing, direction, features, language, stroke_width
            )
            max_width = max(max_width, line_width)
        return max_width, len(lines) * line_spacing - spacing
