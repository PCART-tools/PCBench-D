    def print_tiff(self, filename, *args, **kwargs):
        return self._print_image(filename, wx.BITMAP_TYPE_TIF, *args, **kwargs)
