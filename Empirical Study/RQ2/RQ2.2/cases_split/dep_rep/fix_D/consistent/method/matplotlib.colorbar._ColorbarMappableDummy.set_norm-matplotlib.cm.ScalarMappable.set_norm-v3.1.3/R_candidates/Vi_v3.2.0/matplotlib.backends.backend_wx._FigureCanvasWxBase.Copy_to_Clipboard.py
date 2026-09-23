    def Copy_to_Clipboard(self, event=None):
        "copy bitmap of canvas to system clipboard"
        bmp_obj = wx.BitmapDataObject()
        bmp_obj.SetBitmap(self.bitmap)

        if not wx.TheClipboard.IsOpened():
            open_success = wx.TheClipboard.Open()
            if open_success:
                wx.TheClipboard.SetData(bmp_obj)
                wx.TheClipboard.Close()
                wx.TheClipboard.Flush()
