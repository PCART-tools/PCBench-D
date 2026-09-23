    def render(self, output: Output, x: float, y: float) -> None:
        self.fontset.render_glyph(
            output, x - self._metrics.xmin, y + self._metrics.ymin,
            self.font, self.font_class, self.c, self.fontsize, self.dpi)
