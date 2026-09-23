class GraphicsContextWx(GraphicsContextBase):
    """
    The graphics context provides the color, line styles, etc...

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
        self._style = wx.SOLID
        self.renderer = renderer

    def select(self):
        """
        Select the current bitmap into this wxDC instance
        """

        if sys.platform == 'win32':
            self.dc.SelectObject(self.bitmap)
            self.IsSelected = True

    def unselect(self):
        """
        Select a Null bitmasp into this wxDC instance
        """
        if sys.platform == 'win32':
            self.dc.SelectObject(wx.NullBitmap)
            self.IsSelected = False

    def set_foreground(self, fg, isRGBA=None):
        """
        Set the foreground color.  fg can be a matlab format string, a
        html hex color string, an rgb unit tuple, or a float between 0
        and 1.  In the latter case, grayscale is used.
        """
        # Implementation note: wxPython has a separate concept of pen and
        # brush - the brush fills any outline trace left by the pen.
        # Here we set both to the same colour - if a figure is not to be
        # filled, the renderer will set the brush to be transparent
        # Same goes for text foreground...
        DEBUG_MSG("set_foreground()", 1, self)
        self.select()
        GraphicsContextBase.set_foreground(self, fg, isRGBA)

        self._pen.SetColour(self.get_wxcolour(self.get_rgb()))
        self.gfx_ctx.SetPen(self._pen)
        self.unselect()

    def set_linewidth(self, w):
        """
        Set the line width.
        """
        w = float(w)
        DEBUG_MSG("set_linewidth()", 1, self)
        self.select()
        if 0 < w < 1:
            w = 1
        GraphicsContextBase.set_linewidth(self, w)
        lw = int(self.renderer.points_to_pixels(self._linewidth))
        if lw == 0:
            lw = 1
        self._pen.SetWidth(lw)
        self.gfx_ctx.SetPen(self._pen)
        self.unselect()

    def set_capstyle(self, cs):
        """
        Set the capstyle as a string in ('butt', 'round', 'projecting')
        """
        DEBUG_MSG("set_capstyle()", 1, self)
        self.select()
        GraphicsContextBase.set_capstyle(self, cs)
        self._pen.SetCap(GraphicsContextWx._capd[self._capstyle])
        self.gfx_ctx.SetPen(self._pen)
        self.unselect()

    def set_joinstyle(self, js):
        """
        Set the join style to be one of ('miter', 'round', 'bevel')
        """
        DEBUG_MSG("set_joinstyle()", 1, self)
        self.select()
        GraphicsContextBase.set_joinstyle(self, js)
        self._pen.SetJoin(GraphicsContextWx._joind[self._joinstyle])
        self.gfx_ctx.SetPen(self._pen)
        self.unselect()

    def get_wxcolour(self, color):
        """return a wx.Colour from RGB format"""
        DEBUG_MSG("get_wx_color()", 1, self)
        if len(color) == 3:
            r, g, b = color
            r *= 255
            g *= 255
            b *= 255
            return wx.Colour(red=int(r), green=int(g), blue=int(b))
        else:
            r, g, b, a = color
            r *= 255
            g *= 255
            b *= 255
            a *= 255
            return wx.Colour(
                red=int(r),
                green=int(g),
                blue=int(b),
                alpha=int(a))
