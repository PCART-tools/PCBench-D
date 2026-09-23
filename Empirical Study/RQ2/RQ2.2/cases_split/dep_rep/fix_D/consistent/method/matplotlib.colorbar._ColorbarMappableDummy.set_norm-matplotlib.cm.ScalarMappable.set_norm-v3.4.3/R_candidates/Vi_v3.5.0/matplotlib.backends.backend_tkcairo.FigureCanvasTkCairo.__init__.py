    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._renderer = RendererCairo(self.figure.dpi)
