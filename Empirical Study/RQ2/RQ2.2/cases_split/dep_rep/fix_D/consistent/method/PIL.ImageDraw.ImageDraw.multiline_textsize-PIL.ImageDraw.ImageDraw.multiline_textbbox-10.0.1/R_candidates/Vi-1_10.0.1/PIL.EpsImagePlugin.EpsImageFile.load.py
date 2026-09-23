    def load(self, scale=1, transparency=False):
        # Load EPS via Ghostscript
        if self.tile:
            self.im = Ghostscript(self.tile, self.size, self.fp, scale, transparency)
            self.mode = self.im.mode
            self._size = self.im.size
            self.tile = []
        return Image.Image.load(self)
