    def __init__(self, parent, id, figure):
        # _FigureCanvasWxBase should be fixed to have the same signature as
        # every other FigureCanvas and use cooperative inheritance, but in the
        # meantime the following will make do.
        _FigureCanvasWxBase.__init__(self, parent, id, figure)
        FigureCanvasCairo.__init__(self, figure)
        self._renderer = RendererCairo(self.figure.dpi)
