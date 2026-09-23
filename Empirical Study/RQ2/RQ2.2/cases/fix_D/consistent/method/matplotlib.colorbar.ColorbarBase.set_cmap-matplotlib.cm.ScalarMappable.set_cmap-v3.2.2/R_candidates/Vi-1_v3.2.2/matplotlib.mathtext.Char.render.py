    def render(self, x, y):
        """
        Render the character to the canvas
        """
        self.font_output.render_glyph(
            x, y,
            self.font, self.font_class, self.c, self.fontsize, self.dpi)
