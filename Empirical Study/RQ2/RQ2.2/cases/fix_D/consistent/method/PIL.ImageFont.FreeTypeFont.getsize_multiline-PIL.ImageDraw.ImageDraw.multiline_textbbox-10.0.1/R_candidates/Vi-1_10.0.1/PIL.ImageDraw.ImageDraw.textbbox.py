    def textbbox(
        self,
        xy,
        text,
        font=None,
        anchor=None,
        spacing=4,
        align="left",
        direction=None,
        features=None,
        language=None,
        stroke_width=0,
        embedded_color=False,
    ):
        """Get the bounding box of a given string, in pixels."""
        if embedded_color and self.mode not in ("RGB", "RGBA"):
            msg = "Embedded color supported only in RGB and RGBA modes"
            raise ValueError(msg)

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

        if font is None:
            font = self.getfont()
        mode = "RGBA" if embedded_color else self.fontmode
        bbox = font.getbbox(
            text, mode, direction, features, language, stroke_width, anchor
        )
        return bbox[0] + xy[0], bbox[1] + xy[1], bbox[2] + xy[0], bbox[3] + xy[1]
