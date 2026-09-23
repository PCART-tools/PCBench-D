    def _on_paint(self, event):
        """Called when wxPaintEvt is generated."""
        _log.debug("%s - _on_paint()", type(self))
        drawDC = wx.PaintDC(self)
        if not self._isDrawn:
            self.draw(drawDC=drawDC)
        else:
            self.gui_repaint(drawDC=drawDC)
        drawDC.Destroy()
