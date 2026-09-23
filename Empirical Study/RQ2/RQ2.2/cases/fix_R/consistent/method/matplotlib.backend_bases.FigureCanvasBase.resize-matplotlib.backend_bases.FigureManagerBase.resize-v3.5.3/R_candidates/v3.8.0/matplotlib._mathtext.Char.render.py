    def render(self, output: Output, x: float, y: float) -> None:
        self.fontset.render_glyph(
            output, x, y,
            self.font, self.font_class, self.c, self.fontsize, self.dpi)
