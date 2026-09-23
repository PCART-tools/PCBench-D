    def render(self, output, x, y):
        self.fontset.render_glyph(
            output, x, y,
            self.font, self.font_class, self.c, self.fontsize, self.dpi)
