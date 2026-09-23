    @_api.delete_parameter("3.4", "origin")
    def gui_repaint(self, drawDC=None, origin='WX'):
        """
        Performs update of the displayed image on the GUI canvas, using the
        supplied wx.PaintDC device context.

        The 'WXAgg' backend sets origin accordingly.
        """
        _log.debug("%s - gui_repaint()", type(self))
        # The "if self" check avoids a "wrapped C/C++ object has been deleted"
        # RuntimeError if doing things after window is closed.
        if not (self and self.IsShownOnScreen()):
            return
        if not drawDC:  # not called from OnPaint use a ClientDC
            drawDC = wx.ClientDC(self)
        # For 'WX' backend on Windows, the bitmap can not be in use by another
        # DC (see GraphicsContextWx._cache).
        bmp = (self.bitmap.ConvertToImage().ConvertToBitmap()
               if wx.Platform == '__WXMSW__'
                  and isinstance(self.figure._cachedRenderer, RendererWx)
               else self.bitmap)
        drawDC.DrawBitmap(bmp, 0, 0)
        if self._rubberband_rect is not None:
            x0, y0, x1, y1 = self._rubberband_rect
            drawDC.DrawLineList(
                [(x0, y0, x1, y0), (x1, y0, x1, y1),
                 (x0, y0, x0, y1), (x0, y1, x1, y1)],
                wx.Pen('BLACK', 1, wx.PENSTYLE_SHORT_DASH))
