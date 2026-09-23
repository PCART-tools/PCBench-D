    def __init__(self):
        super().__init__()
        self._texmanager = None
        self._text2path = text.TextToPath()
        self._raster_depth = 0
        self._rasterizing = False
