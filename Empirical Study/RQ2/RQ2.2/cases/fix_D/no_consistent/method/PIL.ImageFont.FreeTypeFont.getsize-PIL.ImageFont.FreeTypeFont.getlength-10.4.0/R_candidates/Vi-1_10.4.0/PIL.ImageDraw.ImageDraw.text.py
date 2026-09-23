    def text(
        self,
        xy: tuple[float, float],
        text: str,
        fill=None,
        font: (
            ImageFont.ImageFont
            | ImageFont.FreeTypeFont
            | ImageFont.TransposedFont
            | None
        ) = None,
        anchor=None,
        spacing=4,
        align="left",
        direction=None,
        features=None,
        language=None,
        stroke_width=0,
        stroke_fill=None,
        embedded_color=False,
        *args,
        **kwargs,
    ) -> None:
        """Draw text."""
        if embedded_color and self.mode not in ("RGB", "RGBA"):
            msg = "Embedded color supported only in RGB and RGBA modes"
            raise ValueError(msg)

        if font is None:
            font = self._getfont(kwargs.get("font_size"))

        if self._multiline_check(text):
            return self.multiline_text(
                xy,
                text,
                fill,
                font,
                anchor,
                spacing,
                align,
                direction,
                features,
                language,
                stroke_width,
                stroke_fill,
                embedded_color,
            )

        def getink(fill: _Ink | None) -> int:
            ink, fill_ink = self._getink(fill)
            if ink is None:
                assert fill_ink is not None
                return fill_ink
            return ink

        def draw_text(ink, stroke_width=0, stroke_offset=None) -> None:
            mode = self.fontmode
            if stroke_width == 0 and embedded_color:
                mode = "RGBA"
            coord = []
            start = []
            for i in range(2):
                coord.append(int(xy[i]))
                start.append(math.modf(xy[i])[0])
            try:
                mask, offset = font.getmask2(  # type: ignore[union-attr,misc]
                    text,
                    mode,
                    direction=direction,
                    features=features,
                    language=language,
                    stroke_width=stroke_width,
                    anchor=anchor,
                    ink=ink,
                    start=start,
                    *args,
                    **kwargs,
                )
                coord = [coord[0] + offset[0], coord[1] + offset[1]]
            except AttributeError:
                try:
                    mask = font.getmask(  # type: ignore[misc]
                        text,
                        mode,
                        direction,
                        features,
                        language,
                        stroke_width,
                        anchor,
                        ink,
                        start=start,
                        *args,
                        **kwargs,
                    )
                except TypeError:
                    mask = font.getmask(text)
            if stroke_offset:
                coord = [coord[0] + stroke_offset[0], coord[1] + stroke_offset[1]]
            if mode == "RGBA":
                # font.getmask2(mode="RGBA") returns color in RGB bands and mask in A
                # extract mask and set text alpha
                color, mask = mask, mask.getband(3)
                ink_alpha = struct.pack("i", ink)[3]
                color.fillband(3, ink_alpha)
                x, y = coord
                if self.im is not None:
                    self.im.paste(
                        color, (x, y, x + mask.size[0], y + mask.size[1]), mask
                    )
            else:
                self.draw.draw_bitmap(coord, mask, ink)

        ink = getink(fill)
        if ink is not None:
            stroke_ink = None
            if stroke_width:
                stroke_ink = getink(stroke_fill) if stroke_fill is not None else ink

            if stroke_ink is not None:
                # Draw stroked text
                draw_text(stroke_ink, stroke_width)

                # Draw normal text
                draw_text(ink, 0)
            else:
                # Only draw normal text
                draw_text(ink)
