class Accent(Char):
    """
    The font metrics need to be dealt with differently for accents,
    since they are already offset correctly from the baseline in
    TrueType fonts.
    """
    def _update_metrics(self):
        metrics = self._metrics = self.font_output.get_metrics(
            self.font, self.font_class, self.c, self.fontsize, self.dpi)
        self.width = metrics.xmax - metrics.xmin
        self.height = metrics.ymax - metrics.ymin
        self.depth = 0

    def shrink(self):
        super().shrink()
        self._update_metrics()

    def grow(self):
        super().grow()
        self._update_metrics()

    def render(self, x, y):
        """
        Render the character to the canvas.
        """
        self.font_output.render_glyph(
            x - self._metrics.xmin, y + self._metrics.ymin,
            self.font, self.font_class, self.c, self.fontsize, self.dpi)
