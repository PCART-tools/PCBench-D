    def __init__(self, width, height, dpi):
        super().__init__()

        self.dpi = dpi
        self.width = width
        self.height = height
        self._renderer = _RendererAgg(int(width), int(height), dpi)
        self._filter_renderers = []

        self._update_methods()
        self.mathtext_parser = MathTextParser('Agg')

        self.bbox = Bbox.from_bounds(0, 0, self.width, self.height)
