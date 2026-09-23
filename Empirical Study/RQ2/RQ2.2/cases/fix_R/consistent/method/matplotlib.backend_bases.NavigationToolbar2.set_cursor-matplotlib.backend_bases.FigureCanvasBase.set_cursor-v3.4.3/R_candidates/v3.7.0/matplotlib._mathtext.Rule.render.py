    def render(self, output, x, y, w, h):
        self.fontset.render_rect_filled(output, x, y, x + w, y + h)
