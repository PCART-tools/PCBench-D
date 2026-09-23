    def polygon(
        self,
        xy: Coords,
        fill: _Ink | None = None,
        outline: _Ink | None = None,
        width: int = 1,
    ) -> None:
        """Draw a polygon."""
        ink, fill_ink = self._getink(outline, fill)
        if fill_ink is not None:
            self.draw.draw_polygon(xy, fill_ink, 1)
        if ink is not None and ink != fill_ink and width != 0:
            if width == 1:
                self.draw.draw_polygon(xy, ink, 0, width)
            elif self.im is not None:
                # To avoid expanding the polygon outwards,
                # use the fill as a mask
                mask = Image.new("1", self.im.size)
                mask_ink = self._getink(1)[0]

                fill_im = mask.copy()
                draw = Draw(fill_im)
                draw.draw.draw_polygon(xy, mask_ink, 1)

                ink_im = mask.copy()
                draw = Draw(ink_im)
                width = width * 2 - 1
                draw.draw.draw_polygon(xy, mask_ink, 0, width)

                mask.paste(ink_im, mask=fill_im)

                im = Image.new(self.mode, self.im.size)
                draw = Draw(im)
                draw.draw.draw_polygon(xy, ink, 0, width)
                self.im.paste(im.im, (0, 0) + im.size, mask.im)
