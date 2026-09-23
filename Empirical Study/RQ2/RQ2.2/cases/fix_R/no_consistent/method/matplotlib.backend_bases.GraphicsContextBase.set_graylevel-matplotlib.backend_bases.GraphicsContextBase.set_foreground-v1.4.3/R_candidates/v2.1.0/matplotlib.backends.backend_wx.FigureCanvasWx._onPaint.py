    def _onPaint(self, evt):
        """
        Called when wxPaintEvt is generated
        """

        DEBUG_MSG("_onPaint()", 1, self)
        drawDC = wx.PaintDC(self)
        if not self._isDrawn:
            self.draw(drawDC=drawDC)
        else:
            self.gui_repaint(drawDC=drawDC)
        evt.Skip()
