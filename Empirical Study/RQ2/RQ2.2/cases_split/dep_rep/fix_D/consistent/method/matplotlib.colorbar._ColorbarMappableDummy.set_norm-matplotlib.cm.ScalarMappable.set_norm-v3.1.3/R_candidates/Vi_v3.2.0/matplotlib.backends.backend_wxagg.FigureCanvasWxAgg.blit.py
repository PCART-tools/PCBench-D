    def blit(self, bbox=None):
        # docstring inherited
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
