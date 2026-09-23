    def blit(self, bbox=None):
        # docstring inherited
        if bbox is None:
            self.bitmap = _convert_agg_to_wx_bitmap(self.get_renderer(), None)
            self.gui_repaint()
            return

        srcBmp = _convert_agg_to_wx_bitmap(self.get_renderer(), None)
        srcDC = wx.MemoryDC()
        srcDC.SelectObject(srcBmp)

        destDC = wx.MemoryDC()
        destDC.SelectObject(self.bitmap)

        x = int(bbox.x0)
        y = int(self.bitmap.GetHeight() - bbox.y1)
        destDC.Blit(x, y, int(bbox.width), int(bbox.height), srcDC, x, y)

        destDC.SelectObject(wx.NullBitmap)
        srcDC.SelectObject(wx.NullBitmap)
        self.gui_repaint()
