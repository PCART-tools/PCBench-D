    def __init__(self, figure):
        super().__init__(figure)
        self._renderer = RendererGTK3Cairo(self.figure.dpi)
