    def _renderer_init(self):
        """Use cairo renderer."""
        self._renderer = RendererGTK3Cairo(self.figure.dpi)
