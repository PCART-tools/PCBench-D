    def print_jpeg(self, filename, *args, **kwargs):
        return self._print_image(filename, wx.BITMAP_TYPE_JPEG,
                                 *args, **kwargs)
