    def load(self):
        if not self.im:
            self.im = Image.core.new(self.mode, self.size)
            self.frombytes(self.fp.read(self._data_size))
        return Image.Image.load(self)
