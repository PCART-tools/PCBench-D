    def __init__(self, bitmap, dpi):
        """Initialise a wxWindows renderer instance."""
        _api.warn_deprecated(
            "2.0", name="wx", obj_type="backend", removal="the future",
            alternative="wxagg", addendum="See the Matplotlib usage FAQ for "
            "more info on backends.")
        super().__init__()
        _log.debug("%s - __init__()", type(self))
        self.width = bitmap.GetWidth()
        self.height = bitmap.GetHeight()
        self.bitmap = bitmap
        self.fontd = {}
        self.dpi = dpi
        self.gc = None
