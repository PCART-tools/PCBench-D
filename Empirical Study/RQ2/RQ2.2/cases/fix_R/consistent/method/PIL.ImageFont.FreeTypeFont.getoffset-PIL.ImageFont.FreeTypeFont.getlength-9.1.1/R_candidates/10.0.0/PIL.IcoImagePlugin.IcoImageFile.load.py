    def load(self):
        if self.im is not None and self.im.size == self.size:
            # Already loaded
            return Image.Image.load(self)
        im = self.ico.getimage(self.size)
        # if tile is PNG, it won't really be loaded yet
        im.load()
        self.im = im.im
        self.pyaccess = None
        self.mode = im.mode
        if im.size != self.size:
            warnings.warn("Image was not the expected size")

            index = self.ico.getentryindex(self.size)
            sizes = list(self.info["sizes"])
            sizes[index] = im.size
            self.info["sizes"] = set(sizes)

            self.size = im.size
