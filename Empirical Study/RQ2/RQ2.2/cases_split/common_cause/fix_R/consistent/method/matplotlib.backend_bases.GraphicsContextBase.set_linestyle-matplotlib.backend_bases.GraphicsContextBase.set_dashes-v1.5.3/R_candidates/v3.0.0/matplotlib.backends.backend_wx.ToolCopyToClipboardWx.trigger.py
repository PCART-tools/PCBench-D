    def trigger(self, *args, **kwargs):
        if not self.canvas._isDrawn:
            self.canvas.draw()
        if not self.canvas.bitmap.IsOk() or not wx.TheClipboard.Open():
            return
        try:
            wx.TheClipboard.SetData(wx.BitmapDataObject(self.canvas.bitmap))
        finally:
            wx.TheClipboard.Close()
