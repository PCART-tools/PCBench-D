class GraphicsContextWx(GraphicsContextBase):
    """
    The graphics context provides the color, line styles, etc.

    This class stores a reference to a wxMemoryDC, and a
    wxGraphicsContext that draws to it.  Creating a wxGraphicsContext
    seems to be fairly heavy, so these objects are cached based on the
    bitmap object that is passed in.

    The base GraphicsContext stores colors as a RGB tuple on the unit
    interval, e.g., (0.5, 0.0, 1.0).  wxPython uses an int interval, but
    since wxPython colour management is rather simple, I have not chosen
    to implement a separate colour manager class.
    """
    _capd = {'butt': wx.CAP_BUTT,
             'projecting': wx.CAP_PROJECTING,
             'round': wx.CAP_ROUND}

    _joind = {'bevel': wx.JOIN_BEVEL,
              'miter': wx.JOIN_MITER,
              'round': wx.JOIN_ROUND}

    _cache = weakref.WeakKeyDictionary()

    def __init__(self, bitmap, renderer):
        super().__init__()
        # assert self.Ok(), "wxMemoryDC not OK to use"
        _log.debug("%s - __init__(): %s", type(self), bitmap)

        dc, gfx_ctx = self._cache.get(bitmap, (None, None))
        if dc is None:
            dc = wx.MemoryDC(bitmap)
            gfx_ctx = wx.GraphicsContext.Create(dc)
            gfx_ctx._lastcliprect = None
            self._cache[bitmap] = dc, gfx_ctx

        self.bitmap = bitmap
        self.dc = dc
        self.gfx_ctx = gfx_ctx
        self._pen = wx.Pen('BLACK', 1, wx.SOLID)
        gfx_ctx.SetPen(self._pen)
        self.renderer = renderer

    def select(self):
        """Select the current bitmap into this wxDC instance."""
        if sys.platform == 'win32':
            self.dc.SelectObject(self.bitmap)
            self.IsSelected = True

    def unselect(self):
        """Select a Null bitmap into this wxDC instance."""
        if sys.platform == 'win32':
            self.dc.SelectObject(wx.NullBitmap)
            self.IsSelected = False

    def set_foreground(self, fg, isRGBA=None):
        # docstring inherited
        # Implementation note: wxPython has a separate concept of pen and
        # brush - the brush fills any outline trace left by the pen.
        # Here we set both to the same colour - if a figure is not to be
        # filled, the renderer will set the brush to be transparent
        # Same goes for text foreground...
        _log.debug("%s - set_foreground()", type(self))
        self.select()
        super().set_foreground(fg, isRGBA)

        self._pen.SetColour(self.get_wxcolour(self.get_rgb()))
        self.gfx_ctx.SetPen(self._pen)
        self.unselect()

    def set_linewidth(self, w):
        # docstring inherited
        w = float(w)
        _log.debug("%s - set_linewidth()", type(self))
        self.select()
        if 0 < w < 1:
            w = 1
        super().set_linewidth(w)
        lw = int(self.renderer.points_to_pixels(self._linewidth))
        if lw == 0:
            lw = 1
        self._pen.SetWidth(lw)
        self.gfx_ctx.SetPen(self._pen)
        self.unselect()

    def set_capstyle(self, cs):
        # docstring inherited
        _log.debug("%s - set_capstyle()", type(self))
        self.select()
        super().set_capstyle(cs)
        self._pen.SetCap(GraphicsContextWx._capd[self._capstyle])
        self.gfx_ctx.SetPen(self._pen)
        self.unselect()

    def set_joinstyle(self, js):
        # docstring inherited
        _log.debug("%s - set_joinstyle()", type(self))
        self.select()
        super().set_joinstyle(js)
        self._pen.SetJoin(GraphicsContextWx._joind[self._joinstyle])
        self.gfx_ctx.SetPen(self._pen)
        self.unselect()

    def get_wxcolour(self, color):
        """Convert a RGB(A) color to a wx.Colour."""
        _log.debug("%s - get_wx_color()", type(self))
        return wx.Colour(*[int(255 * x) for x in color])
