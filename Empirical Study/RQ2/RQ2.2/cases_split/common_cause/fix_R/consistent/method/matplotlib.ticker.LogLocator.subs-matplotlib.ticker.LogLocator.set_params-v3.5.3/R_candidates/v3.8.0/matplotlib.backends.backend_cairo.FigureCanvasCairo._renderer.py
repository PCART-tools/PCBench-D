    @property
    def _renderer(self):
        # In theory, _renderer should be set in __init__, but GUI canvas
        # subclasses (FigureCanvasFooCairo) don't always interact well with
        # multiple inheritance (FigureCanvasFoo inits but doesn't super-init
        # FigureCanvasCairo), so initialize it in the getter instead.
        if not hasattr(self, "_cached_renderer"):
            self._cached_renderer = RendererCairo(self.figure.dpi)
        return self._cached_renderer
