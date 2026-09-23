    def set_linewidth(self, w):
        self._linewidth = float(w)
        self.ctx.set_line_width(self.renderer.points_to_pixels(w))
