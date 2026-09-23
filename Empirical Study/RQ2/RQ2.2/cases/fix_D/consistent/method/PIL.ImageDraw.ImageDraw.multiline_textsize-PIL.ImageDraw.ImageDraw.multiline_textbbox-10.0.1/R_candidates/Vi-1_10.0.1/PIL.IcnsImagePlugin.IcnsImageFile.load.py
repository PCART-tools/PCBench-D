    def load(self):
        if len(self.size) == 3:
            self.best_size = self.size
            self.size = (
                self.best_size[0] * self.best_size[2],
                self.best_size[1] * self.best_size[2],
            )

        px = Image.Image.load(self)
        if self.im is not None and self.im.size == self.size:
            # Already loaded
            return px
        self.load_prepare()
        # This is likely NOT the best way to do it, but whatever.
        im = self.icns.getimage(self.best_size)

        # If this is a PNG or JPEG 2000, it won't be loaded yet
        px = im.load()

        self.im = im.im
        self.mode = im.mode
        self.size = im.size

        return px
