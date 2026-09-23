    def _open(self):
        self.fp.seek(0)  # prep the fp in order to pass the JPEG test
        JpegImagePlugin.JpegImageFile._open(self)
        self._after_jpeg_open()
