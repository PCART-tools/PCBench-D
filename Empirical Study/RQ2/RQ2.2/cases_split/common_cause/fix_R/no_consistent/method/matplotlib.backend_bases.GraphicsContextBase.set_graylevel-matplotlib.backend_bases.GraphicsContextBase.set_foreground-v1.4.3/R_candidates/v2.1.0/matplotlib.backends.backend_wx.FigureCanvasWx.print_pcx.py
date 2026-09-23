    def print_pcx(self, filename, *args, **kwargs):
        return self._print_image(filename, wx.BITMAP_TYPE_PCX, *args, **kwargs)
