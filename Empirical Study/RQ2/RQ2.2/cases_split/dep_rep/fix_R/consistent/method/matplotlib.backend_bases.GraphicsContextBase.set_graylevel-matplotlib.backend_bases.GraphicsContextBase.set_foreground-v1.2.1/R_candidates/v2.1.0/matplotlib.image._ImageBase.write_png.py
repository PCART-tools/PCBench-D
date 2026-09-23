    def write_png(self, fname):
        """Write the image to png file with fname"""
        im = self.to_rgba(self._A[::-1] if self.origin == 'lower' else self._A,
                          bytes=True, norm=True)
        _png.write_png(im, fname)
