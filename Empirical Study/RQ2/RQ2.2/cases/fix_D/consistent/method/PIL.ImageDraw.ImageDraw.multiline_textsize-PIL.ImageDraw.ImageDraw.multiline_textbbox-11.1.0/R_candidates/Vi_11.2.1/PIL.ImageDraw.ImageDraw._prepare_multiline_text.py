    def _prepare_multiline_text(
        self,
        xy: tuple[float, float],
        text: AnyStr,
        font: (
            ImageFont.ImageFont
            | ImageFont.FreeTypeFont
            | ImageFont.TransposedFont
            | None
        ),
        anchor: str | None,
        spacing: float,
        align: str,
        direction: str | None,
        features: list[str] | None,
        language: str | None,
        stroke_width: float,
        embedded_color: bool,
        font_size: float | None,
    ) -> tuple[
        ImageFont.ImageFont | ImageFont.FreeTypeFont | ImageFont.TransposedFont,
        str,
        list[tuple[tuple[float, float], AnyStr]],
    ]:
        if direction == "ttb":
            msg = "ttb direction is unsupported for multiline text"
            raise ValueError(msg)

        if anchor is None:
            anchor = "la"
        elif len(anchor) != 2:
            msg = "anchor must be a 2 character string"
            raise ValueError(msg)
        elif anchor[1] in "tb":
            msg = "anchor not supported for multiline text"
            raise ValueError(msg)

        if font is None:
            font = self._getfont(font_size)

        widths = []
        max_width: float = 0
        lines = text.split("\n" if isinstance(text, str) else b"\n")
        line_spacing = (
            self.textbbox((0, 0), "A", font, stroke_width=stroke_width)[3]
            + stroke_width
            + spacing
        )

        for line in lines:
            line_width = self.textlength(
                line,
                font,
                direction=direction,
                features=features,
                language=language,
                embedded_color=embedded_color,
            )
            widths.append(line_width)
            max_width = max(max_width, line_width)

        top = xy[1]
        if anchor[1] == "m":
            top -= (len(lines) - 1) * line_spacing / 2.0
        elif anchor[1] == "d":
            top -= (len(lines) - 1) * line_spacing

        parts = []
        for idx, line in enumerate(lines):
            left = xy[0]
            width_difference = max_width - widths[idx]

            # first align left by anchor
            if anchor[0] == "m":
                left -= width_difference / 2.0
            elif anchor[0] == "r":
                left -= width_difference

            # then align by align parameter
            if align in ("left", "justify"):
                pass
            elif align == "center":
                left += width_difference / 2.0
            elif align == "right":
                left += width_difference
            else:
                msg = 'align must be "left", "center", "right" or "justify"'
                raise ValueError(msg)

            if align == "justify" and width_difference != 0:
                words = line.split(" " if isinstance(text, str) else b" ")
                word_widths = [
                    self.textlength(
                        word,
                        font,
                        direction=direction,
                        features=features,
                        language=language,
                        embedded_color=embedded_color,
                    )
                    for word in words
                ]
                width_difference = max_width - sum(word_widths)
                for i, word in enumerate(words):
                    parts.append(((left, top), word))
                    left += word_widths[i] + width_difference / (len(words) - 1)
            else:
                parts.append(((left, top), line))

            top += line_spacing

        return font, anchor, parts
