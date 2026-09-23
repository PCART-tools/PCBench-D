    def _renderer_init(self):
        """use cairo renderer"""
        self._renderer = RendererGTK3Cairo(self.figure.dpi)
