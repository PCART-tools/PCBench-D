    def load_prepare(self) -> None:
        # create image memory if necessary
        if self._im is None:
            self.im = Image.core.new(self.mode, self.size)
        # create palette (optional)
        if self.mode == "P":
            Image.Image.load(self)
