    def load(self) -> Image.core.PixelAccess | None:
        if self._im is None:
            self.im = Image.core.new(self.mode, self.size)
            self.frombytes(self.fp.read(self._data_size))
        return Image.Image.load(self)
