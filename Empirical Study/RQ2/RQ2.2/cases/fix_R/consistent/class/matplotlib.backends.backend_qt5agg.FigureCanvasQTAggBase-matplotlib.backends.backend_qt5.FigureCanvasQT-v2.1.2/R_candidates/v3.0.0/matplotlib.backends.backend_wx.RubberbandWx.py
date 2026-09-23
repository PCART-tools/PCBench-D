    class RubberbandWx(backend_tools.RubberbandBase):
        def __init__(self, *args, **kwargs):
            backend_tools.RubberbandBase.__init__(self, *args, **kwargs)
            self._rect = None

        def draw_rubberband(self, x0, y0, x1, y1):
            dc = wx.ClientDC(self.canvas)
            # this would be required if the Canvas is a ScrolledWindow,
            # which is not the case for now
            # self.PrepareDC(dc)

            # delete old rubberband
            if self._rect:
                self.remove_rubberband(dc)

            # draw new rubberband
            dc.SetPen(wx.Pen(wx.BLACK, 1, wx.SOLID))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            self._rect = (x0, self.canvas._height-y0, x1-x0, -y1+y0)
            dc.DrawRectangle(self._rect)

        def remove_rubberband(self, dc=None):
            if not self._rect:
                return
            if self.canvas.bitmap:
                if dc is None:
                    dc = wx.ClientDC(self.canvas)
                dc.DrawBitmap(self.canvas.bitmap, 0, 0)
                #  for testing the method on Windows, use this code instead:
                # img = self.canvas.bitmap.ConvertToImage()
                # bmp = img.ConvertToBitmap()
                # dc.DrawBitmap(bmp, 0, 0)
            self._rect = None
