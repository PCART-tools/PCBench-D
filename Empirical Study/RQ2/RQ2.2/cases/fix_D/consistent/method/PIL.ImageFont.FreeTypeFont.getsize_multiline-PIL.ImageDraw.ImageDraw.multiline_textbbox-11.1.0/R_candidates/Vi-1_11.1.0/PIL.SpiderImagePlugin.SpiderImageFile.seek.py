    def seek(self, frame: int) -> None:
        if self.istack == 0:
            msg = "attempt to seek in a non-stack file"
            raise EOFError(msg)
        if not self._seek_check(frame):
            return
        self.stkoffset = self.hdrlen + frame * (self.hdrlen + self.imgbytes)
        self.fp = self._fp
        self.fp.seek(self.stkoffset)
        self._open()
