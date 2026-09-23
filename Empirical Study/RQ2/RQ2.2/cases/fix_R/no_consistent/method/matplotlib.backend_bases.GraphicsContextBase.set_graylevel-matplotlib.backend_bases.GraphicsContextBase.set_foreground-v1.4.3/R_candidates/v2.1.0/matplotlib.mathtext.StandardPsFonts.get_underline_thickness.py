    def get_underline_thickness(self, font, fontsize, dpi):
        font = self._get_font(font)
        return font.get_underline_thickness() * 0.001 * fontsize
