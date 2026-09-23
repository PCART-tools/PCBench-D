    def __init__(self, bitmap, dpi):
        """Initialise a wxWindows renderer instance."""
        cbook.warn_deprecated(
            "2.0", name="wx", obj_type="backend", removal="the future",
            alternative="wxagg", addendum="See the Matplotlib usage FAQ for "
            "more info on backends.")
        RendererBase.__init__(self)
        DEBUG_MSG("__init__()", 1, self)
        self.width = bitmap.GetWidth()
        self.height = bitmap.GetHeight()
        self.bitmap = bitmap
        self.fontd = {}
        self.dpi = dpi
        self.gc = None
