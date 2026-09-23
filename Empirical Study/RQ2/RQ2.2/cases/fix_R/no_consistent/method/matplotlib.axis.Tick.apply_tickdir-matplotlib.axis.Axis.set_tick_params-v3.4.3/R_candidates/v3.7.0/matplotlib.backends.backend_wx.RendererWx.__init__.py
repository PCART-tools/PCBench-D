    def __init__(self, bitmap, dpi):
        """Initialise a wxWindows renderer instance."""
        super().__init__()
        _log.debug("%s - __init__()", type(self))
        self.width = bitmap.GetWidth()
        self.height = bitmap.GetHeight()
        self.bitmap = bitmap
        self.fontd = {}
        self.dpi = dpi
        self.gc = None
