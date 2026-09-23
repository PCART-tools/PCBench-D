def _convert_agg_to_wx_bitmap(agg, bbox):
    """
    Convert the region of the agg buffer bounded by bbox to a wx.Bitmap.  If
    bbox is None, the entire buffer is converted.
    Note: agg must be a backend_agg.RendererAgg instance.
    """
    if bbox is None:
        # agg => rgba buffer -> bitmap
        return wx.Bitmap.FromBufferRGBA(int(agg.width), int(agg.height),
                                        agg.buffer_rgba())
    else:
        # agg => rgba buffer -> bitmap => clipped bitmap
        srcBmp = wx.Bitmap.FromBufferRGBA(int(agg.width), int(agg.height),
                                          agg.buffer_rgba())
        srcDC = wx.MemoryDC()
        srcDC.SelectObject(srcBmp)

        destBmp = wx.Bitmap(int(bbox.width), int(bbox.height))
        destDC = wx.MemoryDC()
        destDC.SelectObject(destBmp)

        x = int(bbox.x0)
        y = int(int(agg.height) - bbox.y1)
        destDC.Blit(0, 0, int(bbox.width), int(bbox.height), srcDC, x, y)

        srcDC.SelectObject(wx.NullBitmap)
        destDC.SelectObject(wx.NullBitmap)

        return destBmp
