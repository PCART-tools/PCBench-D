    def __init__(self, bitmap, renderer):
        GraphicsContextBase.__init__(self)
        # assert self.Ok(), "wxMemoryDC not OK to use"
        DEBUG_MSG("__init__()", 1, self)
        DEBUG_MSG("__init__() 2: %s" % bitmap, 1, self)

        dc, gfx_ctx = self._cache.get(bitmap, (None, None))
        if dc is None:
            dc = wx.MemoryDC()
            dc.SelectObject(bitmap)
            gfx_ctx = wx.GraphicsContext.Create(dc)
            gfx_ctx._lastcliprect = None
            self._cache[bitmap] = dc, gfx_ctx

        self.bitmap = bitmap
        self.dc = dc
        self.gfx_ctx = gfx_ctx
        self._pen = wx.Pen('BLACK', 1, wx.SOLID)
        gfx_ctx.SetPen(self._pen)
        self.renderer = renderer
