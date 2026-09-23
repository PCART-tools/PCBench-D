    @cbook.deprecated("3.3")
    @property
    def fontangles(self):
        return {
            'italic':  cairo.FONT_SLANT_ITALIC,
            'normal':  cairo.FONT_SLANT_NORMAL,
            'oblique': cairo.FONT_SLANT_OBLIQUE,
        }
