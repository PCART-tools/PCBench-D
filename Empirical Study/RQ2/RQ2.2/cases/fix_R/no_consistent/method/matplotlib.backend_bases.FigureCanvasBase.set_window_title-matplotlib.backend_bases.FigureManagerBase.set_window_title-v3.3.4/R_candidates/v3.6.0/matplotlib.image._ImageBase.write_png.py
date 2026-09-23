    def write_png(self, fname):
        """Write the image to png file *fname*."""
        im = self.to_rgba(self._A[::-1] if self.origin == 'lower' else self._A,
                          bytes=True, norm=True)
        PIL.Image.fromarray(im).save(fname, format="png")
