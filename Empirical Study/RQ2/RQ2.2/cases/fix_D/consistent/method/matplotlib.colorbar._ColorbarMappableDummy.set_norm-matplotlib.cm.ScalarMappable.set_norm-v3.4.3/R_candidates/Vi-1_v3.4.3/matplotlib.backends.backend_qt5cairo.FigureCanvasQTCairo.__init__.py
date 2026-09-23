    def __init__(self, figure=None):
        super().__init__(figure=figure)
        self._renderer = RendererCairo(self.figure.dpi)
        self._renderer.set_width_height(-1, -1)  # Invalid values.
