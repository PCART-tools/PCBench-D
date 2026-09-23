    def gui_repaint(self, drawDC=None, origin='WX'):
        """
        Performs update of the displayed image on the GUI canvas, using the
        supplied wx.PaintDC device context.

        The 'WXAgg' backend sets origin accordingly.
        """
        _log.debug("%s - gui_repaint()", type(self))
        # The "if self" check avoids a "wrapped C/C++ object has been deleted"
        # RuntimeError if doing things after window is closed.
        if self and self.IsShownOnScreen():
            if not drawDC:
                # not called from OnPaint use a ClientDC
                drawDC = wx.ClientDC(self)

            # following is for 'WX' backend on Windows
            # the bitmap can not be in use by another DC,
            # see GraphicsContextWx._cache
            if wx.Platform == '__WXMSW__' and origin == 'WX':
                img = self.bitmap.ConvertToImage()
                bmp = img.ConvertToBitmap()
                drawDC.DrawBitmap(bmp, 0, 0)
            else:
                drawDC.DrawBitmap(self.bitmap, 0, 0)
