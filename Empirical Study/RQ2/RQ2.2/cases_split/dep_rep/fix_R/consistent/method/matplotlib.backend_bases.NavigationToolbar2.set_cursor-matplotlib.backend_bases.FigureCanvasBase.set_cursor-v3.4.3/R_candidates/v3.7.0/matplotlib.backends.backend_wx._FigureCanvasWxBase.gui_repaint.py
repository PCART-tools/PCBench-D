    def gui_repaint(self, drawDC=None):
        """
        Update the displayed image on the GUI canvas, using the supplied
        wx.PaintDC device context.

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
                  and isinstance(self.figure.canvas.get_renderer(), RendererWx)
               else self.bitmap)
        drawDC.DrawBitmap(bmp, 0, 0)
        if self._rubberband_rect is not None:
            # Some versions of wx+python don't support numpy.float64 here.
            x0, y0, x1, y1 = map(round, self._rubberband_rect)
            rect = [(x0, y0, x1, y0), (x1, y0, x1, y1),
                    (x0, y0, x0, y1), (x0, y1, x1, y1)]
            drawDC.DrawLineList(rect, self._rubberband_pen_white)
            drawDC.DrawLineList(rect, self._rubberband_pen_black)
