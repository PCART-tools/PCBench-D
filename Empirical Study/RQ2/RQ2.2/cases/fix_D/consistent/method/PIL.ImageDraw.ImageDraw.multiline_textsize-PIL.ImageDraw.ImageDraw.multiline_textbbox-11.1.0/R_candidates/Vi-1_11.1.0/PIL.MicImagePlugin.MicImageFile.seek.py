    def seek(self, frame: int) -> None:
        if not self._seek_check(frame):
            return
        try:
            filename = self.images[frame]
        except IndexError as e:
            msg = "no such frame"
            raise EOFError(msg) from e

        self.fp = self.ole.openstream(filename)

        TiffImagePlugin.TiffImageFile._open(self)

        self.frame = frame
