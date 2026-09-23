    def _getfont(
        self, font_size: float | None
    ) -> ImageFont.ImageFont | ImageFont.FreeTypeFont | ImageFont.TransposedFont:
        if font_size is not None:
            from . import ImageFont

            return ImageFont.load_default(font_size)
        else:
            return self.getfont()
