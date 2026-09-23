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
