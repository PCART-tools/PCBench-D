    def _render_figure(self, pixmap, width, height):
        self._renderer.set_pixmap (pixmap)
        self._renderer.set_width_height (width, height)
        self.figure.draw (self._renderer)
