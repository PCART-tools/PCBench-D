    def _render_figure(self, pixmap, width, height):
        """used by GTK and GTKcairo. GTKAgg overrides
        """
        self._renderer.set_width_height (width, height)
        self.figure.draw (self._renderer)
