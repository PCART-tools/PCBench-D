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
        deprecate("multiline_textsize", 10, "multiline_textbbox")
        max_width = 0
        lines = self._multiline_split(text)
        line_spacing = self._multiline_spacing(font, spacing, stroke_width)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            for line in lines:
                line_width, line_height = self.textsize(
                    line,
                    font,
                    spacing,
                    direction,
                    features,
                    language,
                    stroke_width,
                )
                max_width = max(max_width, line_width)
        return max_width, len(lines) * line_spacing - spacing
