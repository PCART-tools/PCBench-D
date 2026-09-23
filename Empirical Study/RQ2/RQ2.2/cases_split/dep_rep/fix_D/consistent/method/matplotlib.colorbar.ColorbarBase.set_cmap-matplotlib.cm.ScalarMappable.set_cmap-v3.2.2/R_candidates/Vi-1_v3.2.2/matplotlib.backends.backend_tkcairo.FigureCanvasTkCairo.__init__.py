    def __init__(self, *args, **kwargs):
        super(FigureCanvasTkCairo, self).__init__(*args, **kwargs)
        self._renderer = RendererCairo(self.figure.dpi)
