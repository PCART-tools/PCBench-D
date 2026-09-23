    def _create_bitmap(self):
        """Create a wx.Bitmap from the renderer RGBA buffer"""
        rgba = self.get_renderer().buffer_rgba()
        h, w, _ = rgba.shape
        bitmap = wx.Bitmap.FromBufferRGBA(w, h, rgba)
        bitmap.SetScaleFactor(self.GetDPIScaleFactor())
        return bitmap
