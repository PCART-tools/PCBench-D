    def _getfont(self, font_size: float | None):
        if font_size is not None:
            from . import ImageFont

            font = ImageFont.load_default(font_size)
        else:
            font = self.getfont()
        return font
