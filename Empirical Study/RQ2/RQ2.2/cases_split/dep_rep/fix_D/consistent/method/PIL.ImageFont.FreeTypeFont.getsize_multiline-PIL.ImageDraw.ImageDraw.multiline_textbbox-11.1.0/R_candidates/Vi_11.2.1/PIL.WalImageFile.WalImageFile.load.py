    def load(self) -> Image.core.PixelAccess | None:
        if self._im is None:
            self.im = Image.core.new(self.mode, self.size)
            self.frombytes(self.fp.read(self.size[0] * self.size[1]))
            self.putpalette(quake2palette)
        return Image.Image.load(self)
