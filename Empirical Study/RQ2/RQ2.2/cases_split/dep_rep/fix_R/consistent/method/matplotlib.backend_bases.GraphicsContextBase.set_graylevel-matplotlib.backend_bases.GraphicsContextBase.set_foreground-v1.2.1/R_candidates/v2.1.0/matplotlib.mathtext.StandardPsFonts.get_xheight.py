    def get_xheight(self, font, fontsize, dpi):
        font = self._get_font(font)
        return font.get_xheight() * 0.001 * fontsize
