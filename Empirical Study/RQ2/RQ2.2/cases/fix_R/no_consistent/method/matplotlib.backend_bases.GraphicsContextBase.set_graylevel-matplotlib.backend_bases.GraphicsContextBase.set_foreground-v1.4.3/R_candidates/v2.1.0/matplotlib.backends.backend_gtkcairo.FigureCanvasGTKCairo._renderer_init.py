    def _renderer_init(self):
        """Override to use cairo (rather than GDK) renderer"""
        self._renderer = RendererGTKCairo(self.figure.dpi)
