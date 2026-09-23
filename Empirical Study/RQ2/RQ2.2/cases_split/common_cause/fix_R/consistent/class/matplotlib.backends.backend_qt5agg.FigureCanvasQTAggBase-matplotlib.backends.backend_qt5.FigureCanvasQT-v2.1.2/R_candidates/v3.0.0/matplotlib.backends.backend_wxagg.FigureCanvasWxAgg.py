class FigureCanvasWxAgg(FigureCanvasAgg, _FigureCanvasWxBase):
    """
    The FigureCanvas contains the figure and does event handling.

    In the wxPython backend, it is derived from wxPanel, and (usually)
    lives inside a frame instantiated by a FigureManagerWx. The parent
    window probably implements a wxSizer to control the displayed
    control size - but we give a hint as to our preferred minimum
    size.
    """

    def draw(self, drawDC=None):
        """
        Render the figure using agg.
        """
        FigureCanvasAgg.draw(self)

        self.bitmap = _convert_agg_to_wx_bitmap(self.get_renderer(), None)
        self._isDrawn = True
        self.gui_repaint(drawDC=drawDC, origin='WXAgg')

    def blit(self, bbox=None):
        """
        Transfer the region of the agg buffer defined by bbox to the display.
        If bbox is None, the entire buffer is transferred.
        """
        if bbox is None:
            self.bitmap = _convert_agg_to_wx_bitmap(self.get_renderer(), None)
            self.gui_repaint()
            return

        l, b, w, h = bbox.bounds
        r = l + w
        t = b + h
        x = int(l)
        y = int(self.bitmap.GetHeight() - t)

        srcBmp = _convert_agg_to_wx_bitmap(self.get_renderer(), None)
        srcDC = wx.MemoryDC()
        srcDC.SelectObject(srcBmp)

        destDC = wx.MemoryDC()
        destDC.SelectObject(self.bitmap)

        destDC.Blit(x, y, int(w), int(h), srcDC, x, y)

        destDC.SelectObject(wx.NullBitmap)
        srcDC.SelectObject(wx.NullBitmap)
        self.gui_repaint()

    filetypes = FigureCanvasAgg.filetypes
