    def seek(self, frame: int) -> None:
        if not self._seek_check(frame):
            return
        filename = self.images[frame]
        self.fp = self.ole.openstream(filename)

        TiffImagePlugin.TiffImageFile._open(self)

        self.frame = frame
