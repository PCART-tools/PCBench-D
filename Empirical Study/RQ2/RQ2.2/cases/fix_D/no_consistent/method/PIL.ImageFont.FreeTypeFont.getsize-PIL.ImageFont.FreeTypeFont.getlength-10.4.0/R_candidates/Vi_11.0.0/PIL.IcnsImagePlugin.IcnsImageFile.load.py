    def load(self, scale: int | None = None) -> Image.core.PixelAccess | None:
        if scale is not None or len(self.size) == 3:
            if scale is None and len(self.size) == 3:
                scale = self.size[2]
            assert scale is not None
            width, height = self.size[:2]
            self.size = width * scale, height * scale
            self.best_size = width, height, scale

        px = Image.Image.load(self)
        if self._im is not None and self.im.size == self.size:
            # Already loaded
            return px
        self.load_prepare()
        # This is likely NOT the best way to do it, but whatever.
        im = self.icns.getimage(self.best_size)

        # If this is a PNG or JPEG 2000, it won't be loaded yet
        px = im.load()

        self.im = im.im
        self._mode = im.mode
        self.size = im.size

        return px
