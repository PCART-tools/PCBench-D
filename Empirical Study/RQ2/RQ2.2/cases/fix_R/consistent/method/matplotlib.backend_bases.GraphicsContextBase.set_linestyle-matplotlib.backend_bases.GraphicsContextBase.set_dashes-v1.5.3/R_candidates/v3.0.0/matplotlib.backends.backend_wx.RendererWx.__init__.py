    def __init__(self, bitmap, dpi):
        """
        Initialise a wxWindows renderer instance.
        """
        warn_deprecated('2.0', message="The WX backend is "
                        "deprecated. It's untested "
                        "and will be removed in Matplotlib 3.0. "
                        "Use the WXAgg backend instead. "
                        "See Matplotlib usage FAQ for more info on backends.",
                        alternative='WXAgg')
        RendererBase.__init__(self)
        DEBUG_MSG("__init__()", 1, self)
        self.width = bitmap.GetWidth()
        self.height = bitmap.GetHeight()
        self.bitmap = bitmap
        self.fontd = {}
        self.dpi = dpi
        self.gc = None
