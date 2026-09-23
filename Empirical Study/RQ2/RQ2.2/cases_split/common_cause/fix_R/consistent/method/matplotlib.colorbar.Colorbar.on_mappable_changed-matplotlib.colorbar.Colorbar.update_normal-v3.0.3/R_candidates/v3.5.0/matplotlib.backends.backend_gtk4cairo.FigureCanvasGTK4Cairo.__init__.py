    def __init__(self, figure):
        super().__init__(figure)
        self._renderer = RendererGTK4Cairo(self.figure.dpi)
